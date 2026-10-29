# Videoaula 6 — Filtros complexos e agregações (12 min)

**Objetivo:** montar consultas com vários critérios e gerar relatórios com o *aggregation pipeline* do MongoDB.

| Recurso | Exemplo |
|---|---|
| Igualdade / comparação | `Ticket.status == StatusChamado.ABERTO`, `Ticket.criado_em < limite` |
| Lista contém | `In(Ticket.tags, ["vpn"])` |
| OU / E | `Or(a, b)` / vários critérios no `find(a, b)` |
| Texto | `RegEx(Ticket.titulo, termo, options="i")` |
| Ordenar, paginar | `.sort("-criado_em").skip(n).limit(m)` |
| Agregação | `Ticket.aggregate([{"$group": ...}, {"$sort": ...}])` |

**Arquivo alterado:** [`main.py`](main.py). Os demais vêm da Videoaula 3.

## Como rodar
```powershell
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload
```
Crie alguns chamados com status/prioridades diferentes (via `POST /tickets`) e teste:
`/tickets?status=aberto&prioridade=alta`, `/tickets?tag=vpn`, `/tickets/busca?termo=vpn`,
`/tickets/atrasados?dias=3`, `/relatorios/por-status`, `/relatorios/por-prioridade-e-status`.

## Roteiro de gravação
1. Construir a lista de filtros dinamicamente (só entra o que o usuário informou).
2. Operadores do Beanie (`In`, `Or`, `RegEx`) e o equivalente em `mongosh`.
3. Lembrete: quando existir uma rota `/tickets/{ticket_id}` (como no projeto final), as rotas fixas (`/busca`, `/atrasados`) precisam ser declaradas **antes** dela.
4. Agregação: explicar o pipeline como uma "esteira" (`$match` -> `$group` -> `$sort`).
