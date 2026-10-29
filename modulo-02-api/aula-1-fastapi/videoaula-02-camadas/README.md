# Videoaula 2 — Dividindo as tarefas: Routers e Services (12 min)

**Objetivo:** separar a API em camadas para que cada arquivo tenha uma única responsabilidade.

```
videoaula-02-camadas/
  main.py                     # liga tudo
  routers/tickets.py          # camada HTTP: recebe a requisição e devolve a resposta
  services/ticket_service.py  # camada de negócio: regras e dados (sem saber de HTTP)
  schemas.py                  # contratos Pydantic
```

| Camada | Pergunta que responde | Não deve conhecer |
|---|---|---|
| Router | "Qual rota, verbo e status HTTP?" | Como os dados são guardados |
| Service | "Quais são as regras do chamado?" | Request, Response, status HTTP |

## Como rodar
```powershell
pip install fastapi "uvicorn[standard]" "pydantic[email]"
uvicorn main:app --reload
```

## Roteiro de gravação
1. Começar com **tudo em um único arquivo** (mostrar que cresce e vira bagunça).
2. Extrair `schemas.py`, depois `services/ticket_service.py`, depois `routers/tickets.py` (ao vivo).
3. Usar `APIRouter` e `app.include_router(...)`.
4. Mostrar que o Service pode ser trocado (memória -> MongoDB no Módulo 3) sem alterar o Router.
