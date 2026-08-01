"""
Verifica se existe uma versão mais nova nos Releases do GitHub e,
se confirmado pelo usuário, baixa o novo .exe e substitui o atual —
sem precisar abrir o navegador ou procurar manualmente.

Só funciona no app já empacotado (.exe); rodando via
'python interface.py' não tem exe nenhum pra substituir.

Depende de cada Release no GitHub ter um arquivo .exe anexado
(o mesmo processo manual que já fazemos: Releases > New Release >
anexa o dist/...exe).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

from ui.version import VERSAO

REPOSITORIO_GITHUB = "sankaito/Assistente-Ikuromimy"
URL_API_LATEST = f"https://api.github.com/repos/{REPOSITORIO_GITHUB}/releases/latest"


def executavel_atual() -> str | None:
    """Só faz sentido baixar/aplicar atualização quando o app já está
    rodando como .exe empacotado (sys.frozen)."""
    if getattr(sys, "frozen", False):
        return sys.executable
    return None


def _versao_para_tupla(versao: str) -> tuple[int, ...]:
    versao = versao.strip().lstrip("vV")
    partes = []
    for parte in versao.split("."):
        try:
            partes.append(int(parte))
        except ValueError:
            partes.append(0)
    return tuple(partes)


def existe_versao_mais_nova(versao_remota: str) -> bool:
    return _versao_para_tupla(versao_remota) > _versao_para_tupla(VERSAO)


def verificar_atualizacao() -> dict:
    """Consulta o GitHub. SEMPRE devolve um dicionário no formato:

        {"ok": bool, "atualizacao": dict|None, "erro": str|None}

    - ok=False: a consulta falhou (sem internet, GitHub fora do ar,
      resposta inesperada) — 'erro' tem o motivo, pra mostrar na tela
      em vez de fingir que está tudo bem.
    - ok=True + atualizacao=None: consultou certinho, já está na
      versão mais recente de verdade.
    - ok=True + atualizacao={tag, notas, url_download}: tem uma
      versão nova disponível.
    """
    try:
        requisicao = urllib.request.Request(
            URL_API_LATEST,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "AssistenteVirtualIkuromimy",
            },
        )
        with urllib.request.urlopen(requisicao, timeout=8) as resposta:
            dados = json.loads(resposta.read().decode("utf-8"))
    except Exception as erro:
        return {"ok": False, "atualizacao": None, "erro": f"Não consegui consultar o GitHub: {erro}"}

    tag = dados.get("tag_name", "")
    if not tag:
        return {"ok": False, "atualizacao": None, "erro": "O GitHub respondeu sem nenhuma versão publicada."}

    if not existe_versao_mais_nova(tag):
        return {"ok": True, "atualizacao": None, "erro": None}

    url_exe = None
    for asset in dados.get("assets", []):
        if asset.get("name", "").lower().endswith(".exe"):
            url_exe = asset.get("browser_download_url")
            break

    if not url_exe:
        return {
            "ok": False,
            "atualizacao": None,
            "erro": f"Encontrei a versão {tag}, mas essa Release não tem nenhum .exe anexado.",
        }

    return {
        "ok": True,
        "atualizacao": {"tag": tag, "notas": dados.get("body", ""), "url_download": url_exe},
        "erro": None,
    }


def baixar_atualizacao(url_download: str, progresso=None, tentativas: int = 3) -> str | None:
    """Baixa o .exe novo pra uma pasta temporária. 'progresso', se
    passado, é chamado com (baixado, total) durante o download.
    Devolve o caminho do arquivo baixado, ou None se falhar OU se o
    arquivo ficar incompleto/corrompido mesmo depois de tentar de novo
    (aplicar um .exe incompleto trava o app com erro de DLL faltando).

    Tenta baixar de novo automaticamente até 'tentativas' vezes se o
    arquivo vier corrompido — geralmente resolve casos de rede
    instável cortando o download no meio."""
    destino = Path(tempfile.gettempdir()) / "AssistenteIkuromimy_novo.exe"

    for tentativa in range(1, tentativas + 1):
        try:
            requisicao = urllib.request.Request(
                url_download, headers={"User-Agent": "AssistenteVirtualIkuromimy"}
            )
            with urllib.request.urlopen(requisicao, timeout=15) as resposta:
                total = int(resposta.headers.get("Content-Length", 0))
                baixado = 0
                with open(destino, "wb") as arquivo:
                    while True:
                        bloco = resposta.read(65536)
                        if not bloco:
                            break
                        arquivo.write(bloco)
                        baixado += len(bloco)
                        if progresso:
                            progresso(baixado, total)

            tamanho_final = destino.stat().st_size

            # confere se baixou o arquivo inteiro; um .exe desse app
            # tem dezenas de MB, então algo muito menor também é sinal
            # claro de download incompleto/corrompido
            incompleto = (total > 0 and tamanho_final != total) or tamanho_final < 1_000_000

            if not incompleto:
                return str(destino)

        except Exception:
            pass

        destino.unlink(missing_ok=True)

    return None


def aplicar_atualizacao(caminho_novo_exe: str) -> bool:
    """Substitui o .exe atual pelo baixado e reabre o app sozinho.

    O Windows não deixa um processo apagar/sobrescrever o próprio
    arquivo .exe enquanto ele está rodando — por isso isso é feito
    através de um .bat temporário, chamado logo depois do processo
    atual começar a fechar.

    Em vez de ficar checando via 'tasklist | find' se o processo já
    encerrou (isso trava numa janela presa quando o .bat roda sem
    console visível — o pipe entre os dois comandos quebra), a gente
    só espera um tempo fixo e confia no retry da cópia: se o arquivo
    ainda estiver travado, tenta de novo por até 15 segundos."""
    exe_atual = executavel_atual()
    if not exe_atual:
        return False

    pasta_temp = Path(tempfile.gettempdir())
    script_bat = pasta_temp / "atualizar_ikuromimy.bat"
    log_bat = pasta_temp / "atualizar_ikuromimy.log"

    conteudo_bat = f"""@echo off
setlocal enabledelayedexpansion
echo [%date% %time%] Iniciando atualizacao > "{log_bat}"

echo [%date% %time%] Aguardando o processo antigo fechar... >> "{log_bat}"
timeout /t 3 /nobreak >nul

set TENTATIVAS=0
:copiar
set /a TENTATIVAS+=1
copy /y "{caminho_novo_exe}" "{exe_atual}" >> "{log_bat}" 2>&1
if errorlevel 1 (
    if !TENTATIVAS! LSS 15 (
        echo [%date% %time%] Copia falhou, tentativa !TENTATIVAS! de 15, tentando de novo... >> "{log_bat}"
        timeout /t 1 /nobreak >nul
        goto copiar
    ) else (
        echo [%date% %time%] Copia falhou apos 15 tentativas. Desistindo. >> "{log_bat}"
        exit /b 1
    )
)

echo [%date% %time%] Copia concluida com sucesso. Abrindo o app... >> "{log_bat}"
del "{caminho_novo_exe}" >nul 2>&1
start "" "{exe_atual}"
echo [%date% %time%] Comando de abrir enviado. Finalizando. >> "{log_bat}"
timeout /t 2 /nobreak >nul
del "%~f0"
"""
    script_bat.write_text(conteudo_bat, encoding="utf-8")

    subprocess.Popen(
        ["cmd", "/c", str(script_bat)],
        creationflags=subprocess.CREATE_NO_WINDOW,
    )
    return True
