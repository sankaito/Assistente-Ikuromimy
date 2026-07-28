# Ikuro Assistant

Assistente de desktop com interface gráfica (PySide6), que executa comandos,
toca música, mostra informações do sistema e permite personalizar o tema
do app.

## Requisitos

- Windows (o app usa `pywin32`/WMI pra ler informações de hardware, então
  algumas funções da aba **Sistema** são específicas do Windows)
- Python instalado, com o `pip` disponível

Pra verificar se o Python está instalado, abra o terminal (PowerShell) e rode:

```
py --version
```

Se der erro dizendo que `py` não é reconhecido, instale o Python em
https://www.python.org/downloads/ e marque a opção **"Add python.exe to PATH"**
durante a instalação. Sendo a versão a rodar do python 3.14.6

## Instalação

1. Copie a pasta `projeto` inteira para o computador (não deixe uma pasta
   `projeto` dentro de outra `projeto` — o `interface.py` deve ficar direto
   dentro da pasta, ex: `C:\Users\SEUNOME\projeto\interface.py`).

2. Abra o terminal dentro dessa pasta e instale todas as dependências de
   uma vez com:

   ```
   py -m pip install -r requirements.txt
   ```

   Isso instala tudo que o app precisa: `PySide6` (interface gráfica),
   `psutil` e `pywin32` (informações de sistema), `pyautogui` e `gtts`
   (comandos e voz), `playsound` (tocar áudio) e `wheel` (ferramenta de
   instalação usada por algumas dessas libs).

## Como executar

Dentro da pasta `projeto`, rode:

```
py interface.py
```

### Atalho com duplo clique

Também é possível usar o arquivo `iniciar.bat` (se ele estiver na pasta):
basta dar duplo clique nele. Esse `.bat` entra automaticamente na pasta
onde está e roda o `interface.py`, então funciona não importa em qual
computador ou caminho o projeto esteja.

## Estrutura da pasta

```
projeto/
├── interface.py
├── escravo.py
├── requirements.txt
├── iniciar.bat
└── ui/
    ├── __init__.py
    ├── console.py
    ├── widgets.py          (ColorWheel, usado na aba Configurações)
    ├── sidebar.py           (menu lateral)
    ├── main_window.py       (janela principal, troca as páginas)
    ├── theme_manager.py     (salva/aplica o tema de cor escolhido)
    ├── system_info.py       (coleta dados de hardware do PC)
    └── pages/
        ├── __init__.py
        ├── home_page.py      (comando livre + log)
        ├── music_page.py
        ├── settings_page.py  (escolha de tema/cor)
        └── system_page.py    (mostra processador, RAM, placa de vídeo, disco)
```

## Solução de problemas

**`pip`/`python`/`py` não reconhecido no terminal**
O Python não está instalado ou não foi adicionado ao PATH. Reinstale
marcando "Add python.exe to PATH", feche e abra o terminal de novo.

**`No module named 'X'`**
Alguma dependência não foi instalada. Rode
`py -m pip install -r requirements.txt` novamente, ou instale a lib que
faltou diretamente com `py -m pip install X`.

**`No such file or directory` ao rodar `interface.py`**
Você está numa pasta diferente da que tem o arquivo. Confirme o caminho
com `dir` e entre na pasta certa com `cd CAMINHO\DA\PASTA` antes de
rodar o `py interface.py`.

**Erro ao instalar `playsound`**
Instale a versão fixa `1.2.2`, que não depende de compilação:
`py -m pip install playsound==1.2.2`