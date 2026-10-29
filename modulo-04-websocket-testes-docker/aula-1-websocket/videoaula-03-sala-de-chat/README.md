# Videoaula 3 — Desenvolvendo uma sala de chat de suporte (15 min)

**Objetivo:** integrar o WebSocket ao HelpDesk: cada **chamado é uma sala**, as mensagens ficam salvas no
MongoDB e só o cliente do chamado ou o suporte autenticado entram.

## Arquivos novos/alterados em relação ao Módulo 3
Copiados em [`arquivos/`](arquivos) (mesma estrutura do `projeto-final`, que é onde tudo roda):

| Arquivo | O que faz |
|---|---|
| `app/services/chat_manager.py` | `ConnectionManager` por sala (id do chamado) + `get_chat_manager()` |
| `app/routers/chat.py` | `WS /ws/tickets/{id}` (autenticação, histórico, broadcast) e `GET /chat` |
| `app/static/chat.html` | Cliente web simples (JavaScript puro, sem risco de XSS) |
| `tests/api/test_chat_ws.py` | Testes do chat (veja a Videoaula 5 em diante) |

Além disso, o `TicketService` ganhou **um método** (`app/services/ticket_service.py`):

```python
async def adicionar_mensagem(self, ticket_id, autor: str, texto: str) -> Mensagem:
    ticket = await self.buscar(ticket_id)
    mensagem = Mensagem(autor=autor, texto=texto)
    await ticket.update(Push({Ticket.mensagens: mensagem}))   # $push no MongoDB
    return mensagem
```
E o `main.py` registra o router: `app.include_router(chat.router)`.

## Como rodar (projeto completo)
```powershell
cd ..\..\projeto-final
uvicorn app.main:app --reload
```
1. `POST /tickets` (anote o `id`) e `POST /auth/login` (anote o `access_token`).
2. Abra <http://127.0.0.1:8000/chat> em duas abas: cliente (e-mail do chamado) e suporte (token).

## Roteiro de gravação
1. Desenho: cliente <-> servidor <-> MongoDB; a sala é o `ticket_id`.
2. Mostrar o `ConnectionManager` (já visto) em `chat_manager.py`.
3. Autenticação no handshake: **navegador não envia cabeçalhos** em WebSocket, então o token vai na query string
   (`?token=`). Rejeitar com código `1008` (policy violation).
4. Fluxo: conectar -> enviar histórico -> broadcast de "entrou" -> loop recebendo texto -> gravar -> transmitir.
5. Tratamento de desconexão e conexões quebradas (`transmitir` remove as que falham).
6. Demonstração ao vivo com duas abas.
