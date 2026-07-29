# Assistente Virtual Ikuromimy

Assistente virtual para Windows com comandos por voz/texto, interface
gráfica em PySide6, e automações do dia a dia: tocar música no
Spotify, abrir/fechar programas, pesquisar na web, controlar mídia e
volume, entre outros.

## Funcionalidades

- 🎙 **Comandos por texto**: digite comandos livres como `abrir spotify`, `tocar bohemian rhapsody`, `pesquisar receita de bolo`, `fechar chrome`.
- 🔘 **Atalhos pré-definidos**: botões na tela que executam um comando pronto com um clique só. Vem com atalhos padrão (Spotify, Chrome, Pesquisar, Play/Pause, Próxima) e dá pra criar/remover os seus próprios.
- 💬 **Autocompletar**: sugestões enquanto você digita, baseadas no histórico de comandos, nas palavras-chave conhecidas e nos apps já instalados no PC.
- 🔧 **Autocorreção**: erros de digitação no comando (ex: "abrri" em vez de "abrir") são detectados e corrigidos automaticamente.
- 🧩 **Modos**: grupos de até 5 comandos que executam em sequência com um clique só (ex: "Modo Programador" abre VSCode + Spotify + Claude de uma vez). Crie e remova os seus próprios modos direto pela interface.
- 🎵 **Controle de música**: toca qualquer música pesquisando direto no Spotify, com play/pause, próxima/anterior faixa pelas teclas de mídia do sistema.
- 🚀 **Abertura de qualquer app instalado**: indexa automaticamente os atalhos do Menu Iniciar e o registro do Windows (`App Paths`), então "abrir X" funciona pra praticamente qualquer programa instalado.
- 🎮 **Jogos via protocolo** (Steam, e extensível pra outros launchers): abre direto pelo `steam://`, sem precisar navegar pela lib.
- 🌐 **Pesquisa no navegador**: abre o navegador já pesquisando o termo, com suporte a escolher o motor de busca no próprio comando (`pesquisar no youtube ...`).
- 💻 **Painel de Sistema**: mostra processador, RAM, placa de vídeo e armazenamento do PC.
- 🎨 **Tema personalizável**: roda de cores (estilo HSV) gera um esquema monocromático completo pro app, salvo entre sessões.
- 🔊 **Fala (text-to-speech)**: o assistente responde em voz alta usando gTTS.
- ▶ **Inicialização automática com o Windows** (opcional, configurável na interface).

## Instalação

### Pré-requisitos

- Windows 10/11
- [Python 3.10+](https://python.org) (marcar "Add to PATH" no instalador)

### Rodando a partir do código

```powershell
git clone https://github.com/sankaito/Assistente-Ikuromimy.git
cd Assistente-Ikuromimy

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python interface.py
```

### Gerando o executável (.exe)

Com o ambiente já configurado (passos acima), basta rodar:

```powershell
build.bat
```

Isso gera `dist\Assistente Virtual Ikuromimy.exe` — um executável
standalone, que não depende mais de Python instalado pra rodar.

Pra criar um atalho na Área de Trabalho apontando pra esse `.exe`:

```powershell
python criar_atalho.py
```

## Como usar

Digite comandos no campo de texto, ou clique num dos atalhos
pré-definidos. Alguns exemplos de comando:

| Comando                          | O que faz                                  |
|-----------------------------------|---------------------------------------------|
| `abrir spotify`                   | Abre o Spotify (ou qualquer outro app)      |
| `tocar bohemian rhapsody`         | Pesquisa e toca a música no Spotify         |
| `fechar chrome`                   | Fecha o processo do Chrome                  |
| `pesquisar receita de bolo`       | Abre o navegador já pesquisando             |
| `pesquisar no youtube lofi`       | Pesquisa direto no YouTube                  |
| `play` / `pause`                  | Play/pause da faixa atual                   |
| `próxima` / `anterior`            | Pula/volta faixa                            |
| `aumentar volume` / `diminuir volume` | Ajusta o volume do sistema              |
| `atualizar apps`                  | Reindexação dos apps instalados             |
| `sair`                            | Encerra o assistente                        |

## Estrutura do projeto

```
projeto/
├── interface.py         # ponto de entrada da interface gráfica
├── escravo.py             # lógica de processamento de comandos
├── requirements.txt        # dependências Python
├── ikuro.spec               # receita de empacotamento (PyInstaller)
├── build.bat                  # gera o .exe
├── criar_atalho.py             # cria atalho na Área de Trabalho
│
└── ui/
    ├── main_window.py             # janela principal
    ├── sidebar.py                  # menu lateral
    ├── theme_manager.py             # geração/persistência de tema
    ├── shortcuts_manager.py          # atalhos pré-definidos
    ├── command_history.py             # histórico p/ autocompletar
    ├── modes_manager.py                 # modos (grupos de comandos)
    ├── modes_dialog.py                   # caixa de criação de modos
    ├── modes_executor.py                  # roda os comandos de um modo
    ├── system_info.py                       # coleta info de hardware
    │
    └── pages/
        ├── home_page.py                  # comando livre + atalhos
        ├── music_page.py                  # controle de mídia
        ├── settings_page.py                # tema + inicialização
        ├── system_page.py                   # painel de hardware
        └── modes_page.py                     # aba de Modos
```

## Versionamento

O projeto segue [Versionamento Semântico](https://semver.org/lang/pt-BR/).
Veja o histórico completo de mudanças no [CHANGELOG.md](CHANGELOG.md).

Versão atual: **1.11.0**

## Aviso

Esse assistente automatiza o teclado/mouse do sistema (via
`pyautogui`) pra algumas funções, como buscar músicas no app do
Spotify. Use por sua conta e risco, e evite mexer no PC enquanto um
comando estiver em execução.
