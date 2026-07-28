from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)


class MusicPage(QWidget):
    """Página de controle de música. Usa as mesmas funções que o
    escravo.py já tinha (teclas de mídia do sistema), então funciona
    com Spotify, YouTube Music, ou qualquer player que esteja tocando
    no momento — não precisa o Spotify estar em primeiro plano."""

    def __init__(self):
        super().__init__()

        area = QVBoxLayout(self)

        titulo = QLabel("🎵 Música")
        titulo.setObjectName("titulo")

        subtitulo = QLabel("Controle a reprodução atual")

        botoes_layout = QHBoxLayout()

        self.btn_anterior = QPushButton("⏮ Anterior")
        self.btn_play_pause = QPushButton("⏯ Play / Pause")
        self.btn_proxima = QPushButton("⏭ Próxima")

        for botao in (self.btn_anterior, self.btn_play_pause, self.btn_proxima):
            botao.setMinimumHeight(70)
            botoes_layout.addWidget(botao)

        self.btn_abrir_spotify = QPushButton("Abrir Spotify")
        self.btn_abrir_spotify.setMinimumHeight(45)

        self.status = QLabel("")
        self.status.setObjectName("status_musica")

        self.btn_anterior.clicked.connect(self.faixa_anterior)
        self.btn_play_pause.clicked.connect(self.play_pause)
        self.btn_proxima.clicked.connect(self.proxima_faixa)
        self.btn_abrir_spotify.clicked.connect(self.abrir_spotify)

        area.addWidget(titulo)
        area.addWidget(subtitulo)
        area.addLayout(botoes_layout)
        area.addWidget(self.btn_abrir_spotify)
        area.addWidget(self.status)
        area.addStretch()

    def _executar(self, func, mensagem_sucesso: str) -> None:
        try:
            func()
            self.status.setText(mensagem_sucesso)
        except Exception as erro:
            self.status.setText(f"❌ Erro: {erro}")

    def play_pause(self) -> None:
        import escravo
        self._executar(escravo.media_play_pause, "⏯ Play / Pause enviado")

    def proxima_faixa(self) -> None:
        import escravo
        self._executar(escravo.media_next, "⏭ Próxima faixa")

    def faixa_anterior(self) -> None:
        import escravo
        self._executar(escravo.media_prev, "⏮ Faixa anterior")

    def abrir_spotify(self) -> None:
        import escravo
        self._executar(escravo.focar_janela_spotify, "🎵 Abrindo/focando o Spotify")
