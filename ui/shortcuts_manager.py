"""
Atalhos pré-definidos: botões que executam um comando pronto com um
clique só, sem precisar digitar. Existe uma lista padrão (fixa) e o
usuário pode adicionar os próprios, que ficam salvos entre sessões
via QSettings (mesmo mecanismo do tema e do controle remoto).
"""

from __future__ import annotations

import json

from PySide6.QtCore import QSettings

_ORG = "Ikuromimy"
_APP = "AssistenteVirtual"
_CHAVE_ATALHOS = "atalhos/personalizados"

ATALHOS_PADRAO = [
    {"label": "🎵 Abrir Spotify", "comando": "abrir spotify"},
    {"label": "🌐 Abrir Chrome", "comando": "abrir chrome"},
    {"label": "🔍 Pesquisar", "comando": "pesquisar "},
    {"label": "⏯ Play / Pause", "comando": "play"},
    {"label": "⏭ Próxima faixa", "comando": "próxima"},
]


def listar_atalhos_personalizados() -> list[dict]:
    settings = QSettings(_ORG, _APP)
    bruto = settings.value(_CHAVE_ATALHOS, "")
    if not bruto:
        return []
    try:
        return json.loads(bruto)
    except (json.JSONDecodeError, TypeError):
        return []


def _salvar_atalhos_personalizados(atalhos: list[dict]) -> None:
    settings = QSettings(_ORG, _APP)
    settings.setValue(_CHAVE_ATALHOS, json.dumps(atalhos))


def adicionar_atalho(label: str, comando: str) -> None:
    atalhos = listar_atalhos_personalizados()
    atalhos.append({"label": label, "comando": comando})
    _salvar_atalhos_personalizados(atalhos)


def remover_atalho(label: str) -> None:
    atalhos = listar_atalhos_personalizados()
    atalhos = [a for a in atalhos if a["label"] != label]
    _salvar_atalhos_personalizados(atalhos)


def listar_todos_os_atalhos() -> list[dict]:
    """Padrão primeiro, depois os personalizados do usuário."""
    return ATALHOS_PADRAO + listar_atalhos_personalizados()
