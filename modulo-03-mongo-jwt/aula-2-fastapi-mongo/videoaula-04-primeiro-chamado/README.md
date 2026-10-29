# Videoaula 4 — Salvando o primeiro chamado real no banco e listando a fila (15 min)

**Objetivo:** gravar um chamado no MongoDB pela API e vê-lo aparecer no Atlas e na listagem.

**Arquivos novos/alterados:** [`main.py`](main.py) (rotas `POST /tickets` e `GET /tickets`).
Os demais (`config.py`, `models.py`, `database.py`, `schemas.py`) vêm da Videoaula 3.

## Como rodar
```powershell
pip install -r requirements.txt
copy .env.example .env        # com a sua connection string
python testar_conexao.py
uvicorn main:app --reload
```
No Swagger: `POST /tickets` com
```json
{
  "titulo": "Sem acesso à VPN",
  "descricao": "Desde ontem não consigo conectar na VPN da empresa.",
  "email_solicitante": "ana@empresa.com",
  "prioridade": "alta",
  "tags": ["vpn"]
}
```
Depois `GET /tickets` e confira a coleção `tickets` no Atlas (*Browse Collections*).

## Roteiro de gravação
1. `Ticket(**dados.model_dump())` e `await ticket.insert()`: explicar que o `await` é a conversa com o banco.
2. Mostrar o `id` (ObjectId) gerado e o documento no Atlas.
3. `Ticket.find_all().sort("-criado_em").to_list()`.
4. Por que devolver `TicketOut` e não o `Ticket` (esconder campos internos, `id` como texto).
