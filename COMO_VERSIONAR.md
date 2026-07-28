# Como versionar o projeto

Guia rápido pra usar a partir de agora, toda vez que mexer no código.

## Configuração inicial (só uma vez)

No terminal, dentro da pasta do projeto (onde está o `interface.py`):

```powershell
git init
git add .
git commit -m "chore: início do histórico de versões (v1.9.1)"
git tag v1.9.1
```

Se quiser guardar isso também no GitHub (backup + acesso de qualquer
lugar), cria um repositório vazio lá (sem README/gitignore, pra não
conflitar) e roda:

```powershell
git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPO.git
git branch -M main
git push -u origin main --tags
```

## A cada mudança nova (funcionalidade ou correção de bug)

1. **Atualiza o número da versão** em `ui/version.py`:
   - Corrigiu um bug → sobe o último número (`1.9.1` → `1.9.2`)
   - Adicionou uma funcionalidade nova → sobe o do meio, zera o
     último (`1.9.2` → `1.10.0`)
   - Mudança grande que quebra algo antigo → sobe o primeiro, zera os
     outros (`1.10.0` → `2.0.0`)

2. **Adiciona uma entrada no `CHANGELOG.md`**, no mesmo formato das
   que já existem (uma seção nova `## [x.x.x] — título`, com
   `### Adicionado` e/ou `### Corrigido`).

3. **Commita e marca a tag:**

   ```powershell
   git add .
   git commit -m "feat: descrição curta da funcionalidade"
   git tag v1.10.0
   git push --tags   # se estiver usando GitHub
   ```

   (usa `fix:` no lugar de `feat:` quando for correção de bug — é só
   uma convenção pra deixar o histórico mais fácil de ler, não é
   obrigatório)

## Voltando pra uma versão antiga

Depois que o histórico existir, dá pra ver como o código estava em
qualquer versão marcada:

```powershell
git checkout v1.5.0        # olha como estava (modo "somente leitura")
git checkout main          # volta pro estado atual
```

## Projeto Android (IkuromimyRemoto)

Como é um projeto separado (Android Studio), o ideal é um repositório
Git próprio pra ele, com os mesmos passos acima — o Android Studio já
tem integração com Git embutida (`VCS > Enable Version Control
Integration` no menu, se ainda não tiver feito o `git init` por lá).
