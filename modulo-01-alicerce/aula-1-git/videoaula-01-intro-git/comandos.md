# VIDEOAULA 1 — Comandos (digitar ao vivo)

> **Antes de começar**
> - Use o **PowerShell** ou o **Git Bash** (não o Prompt de Comando antigo): `#` não é comentário no `cmd`.
> - Trabalhe numa pasta sua, por exemplo `cd $HOME\Projects` (nunca em `C:\Windows\System32`).
> - Digite/cole **um comando por vez**. Colar o bloco inteiro de uma vez pode juntar linhas e quebrar comandos.
> - Os comentários (`# ...`) ficam em linhas separadas, acima de cada comando, para você poder copiar só os comandos.

## 0. Configuração inicial (uma única vez na máquina)
```bash
git config --global user.name "Seu Nome"
git config --global user.email "voce@email.com"
git config --global init.defaultBranch main
git --version
```

## 1. Criando o repositório do HelpDesk
```bash
mkdir helpdesk
cd helpdesk
git init
git status
```

## 2. Primeiro commit
```bash
echo "# HelpDesk" > README.md
# arquivo "untracked"
git status
# área de preparação (staging)
git add README.md
# arquivo "staged"
git status
git commit -m "chore: cria README inicial do HelpDesk"
git log --oneline
```

## 3. Branches: trabalhando sem medo
```bash
# cria e entra na branch
git switch -c feature/schema-ticket
echo "TicketCreate em construção" > ticket.txt
git add ticket.txt
git commit -m "feat: adiciona rascunho do schema de chamado"
git log --oneline --graph --all
```

## 4. Voltando para a main e mesclando
```bash
git switch main
git merge feature/schema-ticket
# apaga a branch já mesclada
git branch -d feature/schema-ticket
git log --oneline --graph
```

## 5. Extras úteis (citar rapidamente)
```bash
# o que mudou e ainda não foi para o staging
git diff
# o que está no staging
git diff --staged
# descarta alterações não commitadas de um arquivo
git restore README.md
# detalhes do último commit
git show HEAD
```

## Convenção de mensagens de commit
| Prefixo | Uso |
|---|---|
| `feat:` | nova funcionalidade |
| `fix:` | correção de bug |
| `docs:` | documentação |
| `test:` | testes |
| `chore:` | tarefas de manutenção |
| `refactor:` | refatoração sem mudar comportamento |
