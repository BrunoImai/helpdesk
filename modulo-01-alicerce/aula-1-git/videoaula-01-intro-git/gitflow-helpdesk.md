# Fluxo de branches do HelpDesk

```mermaid
gitGraph
    commit id: "chore: inicia projeto"
    branch develop
    checkout develop
    commit id: "feat: schemas"
    branch feature/ticket-create
    checkout feature/ticket-create
    commit id: "feat: TicketCreate"
    commit id: "test: valida e-mail"
    checkout develop
    merge feature/ticket-create
    checkout main
    merge develop tag: "v0.1.0"
```

| Branch | Função | Regra |
|---|---|---|
| `main` | Código estável, pronto para produção | Ninguém faz commit direto. Só recebe merge da `develop` |
| `develop` | Integração das funcionalidades | Recebe merges de `feature/*` via Pull Request |
| `feature/<nome>` | Uma tarefa por branch | Nasce da `develop`, morre após o merge |
| `hotfix/<nome>` | Correção urgente em produção | Nasce da `main` e volta para `main` e `develop` |

Nomes de branch: `feature/ticket-create`, `feature/login-jwt`, `hotfix/erro-status-chamado`.
