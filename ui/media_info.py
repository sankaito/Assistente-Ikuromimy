"""
Descobre qual música está tocando no momento lendo o título da janela
do Spotify — que fica no formato "Artista - Faixa" enquanto toca algo,
e só "Spotify" quando está parado. Não precisa de nenhuma API key nem
biblioteca exótica, só pywin32 e psutil (que o projeto já usa).

Trade-off consciente: não dá pra pegar a capa do álbum sem a API
oficial do Spotify (que exige cadastro de app + OAuth), então esse
módulo só devolve título/artista/status — a interface mostra um ícone
genérico no lugar da capa.
"""

from __future__ import annotations

import psutil

try:
    import win32gui
    import win32process
    PYWIN32_DISPONIVEL = True
except ImportError:
    PYWIN32_DISPONIVEL = False


def _titulo_janela_spotify() -> str | None:
    if not PYWIN32_DISPONIVEL:
        return None

    titulo_encontrado = None

    def callback(hwnd, _):
        nonlocal titulo_encontrado
        if not win32gui.IsWindowVisible(hwnd):
            return True

        texto = win32gui.GetWindowText(hwnd)
        if not texto:
            return True

        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            processo = psutil.Process(pid)
            if processo.name().lower() == "spotify.exe":
                titulo_encontrado = texto
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

        return True

    win32gui.EnumWindows(callback, None)
    return titulo_encontrado


def obter_info_musica_atual() -> dict | None:
    """Devolve {titulo, artista, capa (sempre None), tocando (bool)}
    lendo o título da janela do Spotify. Devolve None se o Spotify não
    estiver aberto."""
    titulo_janela = _titulo_janela_spotify()
    if not titulo_janela:
        return None

    if titulo_janela.strip().lower() == "spotify":
        return {"titulo": "", "artista": "", "capa": None, "tocando": False}

    if " - " in titulo_janela:
        artista, titulo = titulo_janela.split(" - ", 1)
    else:
        artista, titulo = "", titulo_janela

    return {
        "titulo": titulo.strip(),
        "artista": artista.strip(),
        "capa": None,
        "tocando": True,
    }
