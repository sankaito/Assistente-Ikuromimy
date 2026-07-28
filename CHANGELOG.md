# Changelog — Assistente Virtual Ikuromimy

Todas as mudanças notáveis do projeto, organizadas por versão.
Segue [Versionamento Semântico](https://semver.org/lang/pt-BR/):
`MAJOR.MINOR.PATCH`

- **MAJOR**: mudança grande o suficiente pra quebrar algo que já existia
- **MINOR**: funcionalidade nova, sem quebrar o que já funcionava
- **PATCH**: correção de bug, sem mudar o comportamento esperado

---

## [1.9.1] — Bugfix

### Corrigido
- Tela de conexão do app Android aceitava qualquer chave (o endpoint
  `/ping` não exigia token), fazendo o app achar que tinha conectado
  mesmo com a chave errada — o erro só aparecia depois, ao tentar
  executar um comando de verdade. Agora `/ping` também exige o token
  correto.

## [1.9.0] — Controle Remoto via Android

### Adicionado
- Servidor HTTP local (`ui/remote_server.py`, Flask + werkzeug) rodando
  dentro do app, com endpoints pra receber comandos do celular
  (`/comando`, `/midia/<ação>`, `/sistema`, `/ping`), protegido por
  token de acesso.
- Aba **Controle Remoto** no PC: mostra IP:porta + chave de acesso,
  liga/desliga o servidor.
- App Android nativo (Kotlin, projeto Android Studio completo) com
  tela de conexão e tela de controle (play/pause/próxima/anterior +
  campo de comando livre).
- Inicialização automática com o Windows (checkbox em Configurações,
  `ui/startup_manager.py`).

## [1.8.2] — Bugfix

### Corrigido
- Player iniciava a música e pausava logo em seguida: o `Enter` já
  dava play sozinho no Spotify, e um `media_play_pause()` extra que eu
  tinha adicionado no passo anterior acabava desligando o play que já
  tinha começado. Removido o toggle extra.

## [1.8.1] — Bugfix

### Corrigido
- Comando "tocar" selecionava a **segunda** música do dropdown de
  busca do Spotify em vez da primeira — o código mandava um `"down"`
  extra antes do `"enter"`, pulando o item já destacado por padrão.

## [1.8.0] — Empacotamento e distribuição

### Adicionado
- Empacotamento como `.exe` standalone via PyInstaller (`ikuro.spec`,
  `build.bat`), não depende mais de VS Code/Python instalado.
- Script `criar_atalho.py`: gera atalho na Área de Trabalho.
- Ícone customizado (`icon.ico`) aplicado no `.exe` e no atalho.
- App renomeado de "Ikuro Assistant" pra **"Assistente Virtual
  Ikuromimy"** (título da janela, nome do `.exe`, atalho, configs
  salvas).

### Corrigido
- Caminho relativo do `styles/dark.qss` quebrava dentro do `.exe`
  empacotado (`FileNotFoundError`); agora resolve via `sys._MEIPASS`
  e o arquivo é incluído nos `datas` do `.spec`.
- Aba Sistema tinha sido criada mas nunca conectada no
  `main_window.py`, caindo sempre na tela de Início.

## [1.7.0] — Página Sistema

### Adicionado
- Aba **Sistema**: mostra processador, núcleos, RAM, placa(s) de
  vídeo e armazenamento (`ui/system_info.py` via WMI/psutil,
  `ui/pages/system_page.py`), com botão de atualizar.

## [1.6.0] — Tema personalizável

### Adicionado
- Aba **Configurações**: roda de cores estilo HSV (`ColorWheel` em
  `ui/widgets.py`), gera um esquema monocromático completo (fundo,
  cards, bordas, destaque) a partir de uma cor escolhida
  (`ui/theme_manager.py`), com slider de brilho, campo hex e paleta
  de 5 tons clicáveis. Tema salvo entre sessões via `QSettings`.

## [1.5.0] — Interface gráfica multi-página

### Adicionado
- Estrutura de páginas com `QStackedWidget` (`ui/main_window.py`)
  substituindo a janela única original.
- Sidebar emitindo sinal (`pagina_selecionada`) ao clicar em cada
  botão.
- Aba **Música**: botões ⏮ Anterior / ⏯ Play-Pause / ⏭ Próxima,
  ligados nas teclas de mídia do sistema.

## [1.1.0] — Comando de pesquisa

### Adicionado
- Comando `pesquisar` / `pesquisa` / `buscar` no `escravo.py`: abre o
  navegador já pesquisando o termo (Google por padrão, com suporte a
  trocar de motor no próprio comando, ex: "pesquisar no youtube ...").

## [1.0.0] — Base

### Adicionado
- `escravo.py`: assistente de comandos por voz/texto — abrir/fechar
  programas, tocar música no Spotify, controle de mídia, volume,
  index de aplicativos instalados via atalhos + registro do Windows.
