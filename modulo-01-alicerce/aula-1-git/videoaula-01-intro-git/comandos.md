# VIDEOAULA 1 — Comandos (digitar ao vivo)

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
git status                      # arquivo "untracked"
git add README.md               # área de preparação (staging)
git status                      # arquivo "staged"
git commit -m "chore: cria README inicial do HelpDesk"
git log --oneline
```

## 3. Branches: trabalhando sem medo
```bash
git switch -c feature/schema-ticket     # cria e entra na branch
echo "TicketCreate em construção" > ticket.txt
git add ticket.txt
git commit -m "feat: adiciona rascunho do schema de chamado"
git log --oneline --graph --all
```

## 4. Voltando para a main e mesclando
```bash
git switch main
git merge feature/schema-ticket
git branch -d feature/schema-ticket     # apaga a branch já mesclada
git log --oneline --graph
```

## 5. Extras úteis (citar rapidamente)
```bash
git diff                 # o que mudou e ainda não foi para o staging
git diff --staged        # o que está no staging
git restore arquivo.py   # descarta alterações não commitadas de um arquivo
git show HEAD            # detalhes do último commit
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
