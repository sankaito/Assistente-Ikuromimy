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


def verificar_atualizacao() -> dict | None:
    """Consulta o GitHub. Devolve um dicionário com 'tag', 'notas' e
    'url_download' se tiver uma versão mais nova com um .exe anexado.
    Devolve None se já estiver atualizado, ou se não conseguir
    consultar (sem internet, repositório sem releases, etc.)."""
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

        tag = dados.get("tag_name", "")
        if not tag or not existe_versao_mais_nova(tag):
            return None

        url_exe = None
        for asset in dados.get("assets", []):
            if asset.get("name", "").lower().endswith(".exe"):
                url_exe = asset.get("browser_download_url")
                break

        if not url_exe:
            return None

        return {"tag": tag, "notas": dados.get("body", ""), "url_download": url_exe}
    except Exception:
        return None


def baixar_atualizacao(url_download: str, progresso=None) -> str | None:
    """Baixa o .exe novo pra uma pasta temporária. 'progresso', se
    passado, é chamado com (baixado, total) durante o download.
    Devolve o caminho do arquivo baixado, ou None se falhar."""
    try:
        destino = Path(tempfile.gettempdir()) / "AssistenteIkuromimy_novo.exe"

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

        return str(destino)
    except Exception:
        return None


def aplicar_atualizacao(caminho_novo_exe: str) -> bool:
    """Substitui o .exe atual pelo baixado e reabre o app sozinho.

    O Windows não deixa um processo apagar/sobrescrever o próprio
    arquivo .exe enquanto ele está rodando — por isso isso é feito
    através de um .bat temporário, que espera o processo atual
    encerrar (chamado logo depois daqui), faz a troca, reabre o app,
    e se autodestrói no final."""
    exe_atual = executavel_atual()
    if not exe_atual:
        return False

    nome_exe = os.path.basename(exe_atual)
    script_bat = Path(tempfile.gettempdir()) / "atualizar_ikuromimy.bat"

    conteudo_bat = f"""@echo off
:esperar
tasklist /fi "imagename eq {nome_exe}" | find /i "{nome_exe}" >nul
if not errorlevel 1 (
    timeout /t 1 /nobreak >nul
    goto esperar
)
copy /y "{caminho_novo_exe}" "{exe_atual}" >nul
del "{caminho_novo_exe}" >nul
start "" "{exe_atual}"
del "%~f0"
"""
    script_bat.write_text(conteudo_bat, encoding="utf-8")

    subprocess.Popen(
        ["cmd", "/c", str(script_bat)],
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
    )
    return True
