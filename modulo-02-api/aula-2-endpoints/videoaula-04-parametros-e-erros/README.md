# Videoaula 4 — Lendo a fila: parâmetros de rota, de query e erros humanizados (14 min)

**Objetivo:** receber informação pela URL (rota e query) com validação e devolver erros claros.

**Arquivos:** [`main.py`](main.py)

## Como rodar
```powershell
pip install fastapi "uvicorn[standard]"
uvicorn main:app --reload
```
Teste no navegador / Swagger:
- `/tickets` · `/tickets?status=aberto` · `/tickets?prioridade=alta&limit=2`
- `/tickets/3` · `/tickets/999` (404 humanizado) · `/tickets/0` e `/tickets/abc` (422)
- `/tickets/busca?termo=vpn`

## Roteiro de gravação
1. Parâmetro de **rota** (`/tickets/{ticket_id}`) vs. de **query** (`?status=aberto`).
2. Validação com `Path(ge=1)` e `Query(max_length=...)`.
3. `Enum` como parâmetro: o Swagger mostra uma lista de opções.
4. `HTTPException(404)` com mensagem amigável.
5. **Cuidado com a ordem das rotas:** `/tickets/busca` precisa vir antes de `/tickets/{ticket_id}`.
6. Handler global para padronizar o formato do erro de validação (422).
