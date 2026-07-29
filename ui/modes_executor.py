"""
Executa a lista de comandos de um modo, um atrás do outro, numa
thread separada — pra não travar a interface enquanto os comandos
rodam (alguns, como tocar música, têm esperas de vários segundos).
"""

from __future__ import annotations

import time

from PySide6.QtCore import QThread

# pausa entre um comando e o próximo do mesmo modo, pra dar tempo do
# comando anterior (ex: abrir um app) se estabilizar antes do próximo
PAUSA_ENTRE_COMANDOS = 0.6


class ExecutorModo(QThread):

    def __init__(self, comandos: list[str], parent=None):
        super().__init__(parent)
        self.comandos = comandos

    def run(self) -> None:
        import escravo

        for comando in self.comandos:
            try:
                escravo.processar_comando(comando)
            except Exception as erro:
                print(f"⚠️ Erro executando \"{comando}\" dentro do modo: {erro}")
            time.sleep(PAUSA_ENTRE_COMANDOS)
