# Videoaula 2 — Repositórios remotos e boas práticas (10 min)

**Objetivo:** conectar o repositório local ao GitHub e colaborar sem quebrar o código dos colegas.

**Arquivos**
- [`comandos.md`](comandos.md): remotos, push/pull, Pull Request e resolução de conflito.
- [`.gitignore`](.gitignore): modelo de `.gitignore` para projetos Python.
- [`PULL_REQUEST_TEMPLATE.md`](PULL_REQUEST_TEMPLATE.md): modelo de PR (vai em `.github/` no repositório).

## Roteiro de gravação
1. Criar o repositório vazio no GitHub (sem README, para evitar conflito inicial).
2. `git remote add origin` + `git push -u origin main`.
3. Simular colega: criar commit no GitHub e fazer `git pull`.
4. Provocar um conflito de propósito e resolvê-lo (bloco 4 de `comandos.md`).
5. Boas práticas: commits pequenos, branch por tarefa, `pull` antes de `push`, nunca versionar `.env`, PR com revisão.
