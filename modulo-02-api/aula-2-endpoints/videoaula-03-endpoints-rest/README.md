# Videoaula 3 — Endpoints semânticos: GET, POST, PUT, DELETE (12 min)

**Objetivo:** construir o CRUD do HelpDesk escolhendo o verbo HTTP e o status code corretos para cada ação.

| Ação do usuário | Verbo | Rota | Status de sucesso |
|---|---|---|---|
| Listar chamados | GET | `/tickets` | 200 |
| Consultar um chamado | GET | `/tickets/{id}` | 200 |
| Abrir um chamado | POST | `/tickets` | 201 |
| Substituir os dados | PUT | `/tickets/{id}` | 200 |
| Deletar um chamado | DELETE | `/tickets/{id}` | 204 |

**Arquivos:** [`main.py`](main.py)

## Como rodar
```powershell
pip install fastapi "uvicorn[standard]" "pydantic[email]"
uvicorn main:app --reload
```

## Roteiro de gravação
1. Substantivos no plural na rota (`/tickets`), verbos no método HTTP (nunca `/criarTicket`).
2. Implementar GET e POST; mostrar `status_code=201`.
3. Implementar PUT (substitui tudo) e explicar a diferença para PATCH (altera parte).
4. Implementar DELETE com `204 No Content` (resposta sem corpo).
5. Testar tudo no Swagger.
