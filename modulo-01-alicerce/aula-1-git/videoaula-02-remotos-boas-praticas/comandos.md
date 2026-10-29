# VIDEOAULA 2 — Comandos (digitar ao vivo)

## 1. Conectando ao GitHub
```bash
# Repositório criado vazio no GitHub: https://github.com/<usuario>/helpdesk
git remote add origin https://github.com/<usuario>/helpdesk.git
git remote -v
git push -u origin main        # -u liga a branch local à remota
```

## 2. Rotina diária (sempre nesta ordem)
```bash
git switch main
git pull origin main                       # 1. traz o que os colegas fizeram
git switch -c feature/ticket-create        # 2. branch para a sua tarefa
# ... edita arquivos ...
git add .
git commit -m "feat: cria schema TicketCreate"
git push -u origin feature/ticket-create   # 3. envia a branch
# 4. abre o Pull Request no GitHub e pede revisão
```

## 3. Clonando o projeto de outra pessoa
```bash
git clone https://github.com/<usuario>/helpdesk.git
cd helpdesk
git branch -a
```

## 4. Provocando e resolvendo um conflito (demonstração)
```bash
git switch -c feature/titulo-a
echo "titulo = 'Chamado A'" > config.py
git add . && git commit -m "feat: titulo A"

git switch main
git switch -c feature/titulo-b
echo "titulo = 'Chamado B'" > config.py
git add . && git commit -m "feat: titulo B"

git merge feature/titulo-a          # CONFLICT (content): Merge conflict in config.py
```
O arquivo ficará assim:
```text
<<<<<<< HEAD
titulo = 'Chamado B'
=======
titulo = 'Chamado A'
>>>>>>> feature/titulo-a
```
Resolução: editar o arquivo deixando a versão correta, remover os marcadores e então:
```bash
git add config.py
git commit -m "fix: resolve conflito no titulo"
```

## 5. Desfazendo com segurança
```bash
git restore --staged arquivo.py     # tira do staging
git restore arquivo.py              # descarta alterações locais
git revert <hash>                   # cria commit que desfaz outro (seguro para histórico compartilhado)
```
> Evite `git push --force` em branches compartilhadas. Isso reescreve o histórico dos colegas.

## 6. Boas práticas (resumo para a tela final)
- Commits pequenos, com mensagem clara (`feat:`, `fix:`...).
- Uma branch por tarefa; nunca commitar direto na `main`.
- `git pull` antes de começar e antes de `push`.
- Nunca versionar `.env`, senhas, tokens ou `.venv`.
- Pull Request com descrição e revisão de pelo menos uma pessoa.
