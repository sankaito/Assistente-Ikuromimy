from PySide6.QtCore import Qt, QStringListModel
from PySide6.QtWidgets import (
    QCompleter,
    QGridLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ui import command_history, shortcuts_manager

COLUNAS_ATALHOS = 4


class HomePage(QWidget):
    """Página inicial: atalhos pré-definidos (um clique executa),
    campo de comando livre com autocompletar/sugestão + log."""

    def __init__(self):
        super().__init__()

        area = QVBoxLayout(self)

        titulo = QLabel("🤖 Assistente Virtual Ikuromimy")
        titulo.setObjectName("titulo")

        subtitulo = QLabel("Digite um comando ou clique em um atalho")

        # -- atalhos pré-definidos ------------------------------------------
        area.addWidget(titulo)
        area.addWidget(subtitulo)

        self.grid_atalhos = QGridLayout()
        area.addLayout(self.grid_atalhos)
        self._montar_atalhos()

        # -- campo de comando com autocompletar ------------------------------
        self.comando = QLineEdit()
        self.comando.setPlaceholderText("Ex: abrir spotify...")
        self.comando.returnPressed.connect(self.executar_comando)

        self._completer = QCompleter()
        self._completer.setCaseSensitivity(Qt.CaseInsensitive)
        self._completer.setFilterMode(Qt.MatchContains)
        self.comando.setCompleter(self._completer)
        self._atualizar_sugestoes()

        botao = QPushButton("▶ Executar")
        botao.clicked.connect(self.executar_comando)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.append("Sistema iniciado...")

        area.addWidget(self.comando)
        area.addWidget(botao)
        area.addWidget(self.log)

    # ----------------------------------------------------------------
    # atalhos pré-definidos
    # ----------------------------------------------------------------

    def _montar_atalhos(self) -> None:
        while self.grid_atalhos.count():
            item = self.grid_atalhos.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        atalhos = shortcuts_manager.listar_todos_os_atalhos()
        personalizados = {a["label"] for a in shortcuts_manager.listar_atalhos_personalizados()}

        for i, atalho in enumerate(atalhos):
            botao = QPushButton(atalho["label"])
            botao.clicked.connect(
                lambda checked=False, c=atalho["comando"]: self._executar_texto(c)
            )

            if atalho["label"] in personalizados:
                botao.setContextMenuPolicy(Qt.CustomContextMenu)
                botao.customContextMenuRequested.connect(
                    lambda pos, l=atalho["label"], b=botao: self._menu_remover_atalho(l, b, pos)
                )

            linha, coluna = divmod(i, COLUNAS_ATALHOS)
            self.grid_atalhos.addWidget(botao, linha, coluna)

        # botão de adicionar, sempre por último
        total = len(atalhos)
        linha, coluna = divmod(total, COLUNAS_ATALHOS)
        botao_add = QPushButton("+ Novo atalho")
        botao_add.clicked.connect(self._adicionar_atalho)
        self.grid_atalhos.addWidget(botao_add, linha, coluna)

    def _menu_remover_atalho(self, label: str, botao: QPushButton, pos) -> None:
        menu = QMenu(self)
        acao_remover = menu.addAction("Remover atalho")
        escolhida = menu.exec(botao.mapToGlobal(pos))
        if escolhida == acao_remover:
            shortcuts_manager.remover_atalho(label)
            self._montar_atalhos()

    def _adicionar_atalho(self) -> None:
        label, ok = QInputDialog.getText(self, "Novo atalho", "Nome do botão (ex: 🎮 Abrir Steam):")
        if not ok or not label.strip():
            return

        comando, ok = QInputDialog.getText(self, "Novo atalho", "Comando a executar (ex: abrir steam):")
        if not ok or not comando.strip():
            return

        shortcuts_manager.adicionar_atalho(label.strip(), comando.strip())
        self._montar_atalhos()

    # ----------------------------------------------------------------
    # autocompletar
    # ----------------------------------------------------------------

    def _atualizar_sugestoes(self) -> None:
        sugestoes = [
            "tocar ", "pesquisar ", "abrir ", "fechar ",
            "play", "pause", "próxima", "anterior",
            "aumentar volume", "diminuir volume",
            "atualizar apps", "sair",
        ]

        try:
            import escravo
            for nome in escravo.listar_apps_conhecidos():
                sugestoes.append(f"abrir {nome}")
        except Exception:
            pass

        # histórico primeiro (mais relevante), sem duplicar
        historico = command_history.carregar_historico()
        sugestoes = historico + [s for s in sugestoes if s not in historico]

        self._completer.setModel(QStringListModel(sugestoes, self._completer))

    # ----------------------------------------------------------------
    # execução
    # ----------------------------------------------------------------

    def _executar_texto(self, texto: str) -> None:
        self.comando.setText(texto)
        self.executar_comando()

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
                command_history.adicionar_ao_historico(comando)
                self._atualizar_sugestoes()
            else:
                self.log.append("Assistente encerrado\n")

        except Exception as erro:
            self.log.append(f"❌ Erro: {erro}")
