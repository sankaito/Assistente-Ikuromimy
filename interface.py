import os
import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


def resource_path(caminho_relativo: str) -> str:
    """Resolve um caminho relativo tanto rodando 'python interface.py'
    quanto rodando o .exe empacotado pelo PyInstaller. No .exe, os
    arquivos de dados (como styles/dark.qss) ficam extraídos numa pasta
    temporária apontada por sys._MEIPASS — que só existe quando o app
    está "congelado" (frozen) pelo PyInstaller."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, caminho_relativo)


def main() -> None:
    app = QApplication(sys.argv)

    caminho_qss = resource_path(os.path.join("styles", "dark.qss"))
    try:
        with open(caminho_qss, "r", encoding="utf-8") as arquivo:
            app.setStyleSheet(arquivo.read())
    except FileNotFoundError:
        # não é fatal: a página de Configurações aplica um tema por
        # cima assim que a MainWindow abre, então o app continua com
        # uma aparência normal mesmo sem esse arquivo.
        print(f"⚠️ Não encontrei {caminho_qss}, seguindo sem o estilo base.")

    janela = MainWindow()
    janela.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
