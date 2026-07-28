from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget,
)

from ui.sidebar import Sidebar
from ui.pages.home_page import HomePage
from ui.pages.music_page import MusicPage
from ui.pages.settings_page import SettingsPage
from ui.pages.system_page import SystemPage
from ui.pages.remote_page import RemotePage
from ui import theme_manager


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Assistente Virtual Ikuromimy")
        self.resize(1100, 700)

        # reaplica o tema escolhido numa sessão anterior (ou o padrão,
        # se o usuário nunca personalizou nada ainda)
        theme_manager.aplicar_tema(theme_manager.carregar_cor())

        self.criar_interface()

    def criar_interface(self):

        principal = QWidget()
        self.setCentralWidget(principal)

        layout = QHBoxLayout(principal)

        # MENU LATERAL
        self.sidebar = Sidebar()
        self.sidebar.pagina_selecionada.connect(self.trocar_pagina)
        layout.addWidget(self.sidebar)

        # PÁGINAS (troca só a parte da direita, sidebar fica fixa)
        self.paginas = QStackedWidget()

        self.pagina_inicio = HomePage()
        self.pagina_musica = MusicPage()
        self.pagina_config = SettingsPage()
        self.pagina_sistema = SystemPage()
        self.pagina_remoto = RemotePage()

        self.paginas.addWidget(self.pagina_inicio)
        self.paginas.addWidget(self.pagina_musica)
        self.paginas.addWidget(self.pagina_config)
        self.paginas.addWidget(self.pagina_sistema)
        self.paginas.addWidget(self.pagina_remoto)

        # mapa chave -> página, pra achar rápido quando a sidebar avisar
        self._mapa_paginas = {
            "inicio": self.pagina_inicio,
            "musica": self.pagina_musica,
            "config": self.pagina_config,
            "sistema": self.pagina_sistema,
            "remoto": self.pagina_remoto,
        }

        layout.addWidget(self.paginas)

    def trocar_pagina(self, chave: str) -> None:
        pagina = self._mapa_paginas.get(chave, self.pagina_inicio)
        self.paginas.setCurrentWidget(pagina)
