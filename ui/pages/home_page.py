from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
)


class HomePage(QWidget):
    """Página inicial: campo de comando livre + log, executando tudo
    através do escravo.processar_comando (igual já funcionava antes)."""

    def __init__(self):
        super().__init__()

        area = QVBoxLayout(self)

        titulo = QLabel("🤖 Assistente Virtual Ikuromimy")
        titulo.setObjectName("titulo")

        subtitulo = QLabel("Digite um comando para executar")

        self.comando = QLineEdit()
        self.comando.setPlaceholderText("Ex: abrir spotify...")

        botao = QPushButton("▶ Executar")
        botao.clicked.connect(self.executar_comando)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.append("Sistema iniciado...")

        area.addWidget(titulo)
        area.addWidget(subtitulo)
        area.addWidget(self.comando)
        area.addWidget(botao)
        area.addWidget(self.log)

    def executar_comando(self):
        comando = self.comando.text()

        if not comando.strip():
            return

        self.log.append(f"Você: {comando}")

        try:
            import escravo

            continuar = escravo.processar_comando(comando)

            if continuar:
                self.log.append("✓ Comando executado\n")
            else:
                self.log.append("Assistente encerrado\n")

        except Exception as erro:
            self.log.append(f"❌ Erro: {erro}")
