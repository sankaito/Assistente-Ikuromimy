from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from ui.modes_manager import LIMITE_COMANDOS_POR_MODO


class CriarModoDialog(QDialog):
    """Caixa de criação: nome do modo + campos de comando, com um
    botão '+' pra adicionar mais (até o limite de 5)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Criar modo")
        self.setMinimumWidth(360)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Nome do modo (ex: 🧑‍💻 Modo Programador):"))
        self.campo_nome = QLineEdit()
        layout.addWidget(self.campo_nome)

        layout.addWidget(QLabel("Comandos (executam em sequência, um por vez):"))

        self._layout_comandos = QVBoxLayout()
        layout.addLayout(self._layout_comandos)

        self.campos_comando: list[QLineEdit] = []
        self._adicionar_campo_comando()

        self.btn_adicionar = QPushButton("+ Adicionar comando")
        self.btn_adicionar.clicked.connect(self._adicionar_campo_comando)
        layout.addWidget(self.btn_adicionar)

        botoes = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        botoes.accepted.connect(self.accept)
        botoes.rejected.connect(self.reject)
        layout.addWidget(botoes)

    def _adicionar_campo_comando(self) -> None:
        if len(self.campos_comando) >= LIMITE_COMANDOS_POR_MODO:
            return

        campo = QLineEdit()
        campo.setPlaceholderText(f"Comando {len(self.campos_comando) + 1} (ex: abrir spotify)")
        self._layout_comandos.addWidget(campo)
        self.campos_comando.append(campo)

        if len(self.campos_comando) >= LIMITE_COMANDOS_POR_MODO:
            self.btn_adicionar.setEnabled(False)
            self.btn_adicionar.setText("Limite de 5 comandos atingido")

    def dados(self) -> tuple[str, list[str]]:
        """Devolve (nome, lista_de_comandos) com o que foi digitado."""
        nome = self.campo_nome.text().strip()
        comandos = [c.text().strip() for c in self.campos_comando if c.text().strip()]
        return nome, comandos
