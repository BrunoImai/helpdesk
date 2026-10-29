# Videoaula 5 — Atualizando status e deletando chamados (CRUD completo) (12 min)

**Objetivo:** completar o CRUD com `get`, `set` e `delete` do Beanie.

| Operação | HTTP | Beanie |
|---|---|---|
| Create | `POST /tickets` | `await ticket.insert()` |
| Read (lista) | `GET /tickets` | `await Ticket.find_all().to_list()` |
| Read (um) | `GET /tickets/{id}` | `await Ticket.get(id)` |
| Update parcial | `PATCH /tickets/{id}/status` | `await ticket.set({...})` |
| Update total | `PUT /tickets/{id}` | `await ticket.set({...})` com todos os campos |
| Delete | `DELETE /tickets/{id}` | `await ticket.delete()` |

**Arquivo alterado:** [`main.py`](main.py). Os demais vêm da Videoaula 3.

## Como rodar
```powershell
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload
```
Teste a sequência no Swagger: criar -> copiar o `id` -> consultar -> mudar status -> apagar -> consultar de novo (404).

## Roteiro de gravação
1. `PydanticObjectId` como tipo do parâmetro de rota: um id inválido já vira 422 automaticamente.
2. Função auxiliar `buscar_ou_404` (evita repetição).
3. `set` envia apenas `$set` ao Mongo (não reescreve o documento todo).
4. Tratamento do "não encontrado". (No projeto final isso vira uma exceção de serviço + handler global.)
