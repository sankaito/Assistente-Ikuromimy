"""
Modos: grupos de até 5 comandos que executam em sequência com um
clique só (ex: "🧑‍💻 Modo Programador" abre VSCode + Spotify + Claude
de uma vez). Persistidos via QSettings, mesmo mecanismo dos atalhos.
"""

from __future__ import annotations

import json

from PySide6.QtCore import QSettings

_ORG = "Ikuromimy"
_APP = "AssistenteVirtual"
_CHAVE_MODOS = "modos/personalizados"

LIMITE_COMANDOS_POR_MODO = 5


def listar_modos() -> list[dict]:
    settings = QSettings(_ORG, _APP)
    bruto = settings.value(_CHAVE_MODOS, "")
    if not bruto:
        return []
    try:
        return json.loads(bruto)
    except (json.JSONDecodeError, TypeError):
        return []


def _salvar_modos(modos: list[dict]) -> None:
    settings = QSettings(_ORG, _APP)
    settings.setValue(_CHAVE_MODOS, json.dumps(modos))


def adicionar_modo(nome: str, comandos: list[str]) -> None:
    comandos = [c.strip() for c in comandos if c.strip()][:LIMITE_COMANDOS_POR_MODO]
    if not nome.strip() or not comandos:
        return

    modos = listar_modos()
    modos.append({"nome": nome.strip(), "comandos": comandos})
    _salvar_modos(modos)


def remover_modo(nome: str) -> None:
    modos = listar_modos()
    modos = [m for m in modos if m["nome"] != nome]
    _salvar_modos(modos)
