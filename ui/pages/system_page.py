from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ui import system_info


class SystemPage(QWidget):
    """Aba Sistema: mostra processador, RAM, placa de vídeo e
    armazenamento do PC em cards. Lê tudo assim que a página é criada;
    o botão 'Atualizar' relê na hora (útil pro uso de RAM/disco, que
    muda com o tempo)."""

    def __init__(self):
        super().__init__()

        area = QVBoxLayout(self)

        titulo = QLabel("💻 Sistema")
        titulo.setObjectName("titulo")

        subtitulo = QLabel("Informações de hardware do seu PC")

        self.btn_atualizar = QPushButton("🔄 Atualizar")
        self.btn_atualizar.clicked.connect(self._carregar)

        area.addWidget(titulo)
        area.addWidget(subtitulo)
        area.addWidget(self.btn_atualizar, alignment=Qt.AlignLeft)

        self._grid = QGridLayout()
        self._grid.setHorizontalSpacing(16)
        self._grid.setVerticalSpacing(16)
        area.addLayout(self._grid)

        area.addStretch()

        self._carregar()

    # ------------------------------------------------------------------

    def _limpar_grid(self) -> None:
        while self._grid.count():
            item = self._grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def _card(self, titulo_texto: str, linhas: list[str]) -> QFrame:
        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)

        rotulo_titulo = QLabel(titulo_texto)
        rotulo_titulo.setStyleSheet("font-weight: 600; font-size: 15px;")
        layout.addWidget(rotulo_titulo)

        if not linhas:
            layout.addWidget(QLabel("Não foi possível detectar"))
        else:
            for linha in linhas:
                rotulo = QLabel(linha)
                rotulo.setWordWrap(True)
                layout.addWidget(rotulo)

        return card

    def _carregar(self) -> None:
        self._limpar_grid()

        info = system_info.obter_resumo_sistema()

        card_cpu = self._card(
            "🧠 Processador",
            [info["processador"], info["nucleos"]],
        )

        card_ram = self._card(
            "💾 Memória RAM",
            [f"Total: {info['ram']['total']}", info["ram"]["uso"]],
        )

        card_gpu = self._card(
            "🎮 Placa de Vídeo",
            info["placas_de_video"],
        )

        linhas_disco = [
            f"{d['unidade']}  —  {d['total']}  ({d['usado']})"
            for d in info["armazenamento"]
        ] or ["Nenhuma unidade detectada"]

        card_disco = self._card("🗄 Armazenamento", linhas_disco)

        self._grid.addWidget(card_cpu, 0, 0)
        self._grid.addWidget(card_ram, 0, 1)
        self._grid.addWidget(card_gpu, 1, 0)
        self._grid.addWidget(card_disco, 1, 1)
