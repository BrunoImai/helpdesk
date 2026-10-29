# Videoaula 7 — Os gerentes do tráfego: WSGI vs. ASGI (Uvicorn) (10 min)

**Objetivo:** entender que o servidor (Uvicorn, Gunicorn) conversa com o código Python por uma interface padrão.

| | WSGI | ASGI |
|---|---|---|
| Ano / ideia | 2003, "uma requisição por vez por worker" | 2016+, assíncrono |
| Função da aplicação | `app(environ, start_response)` | `async app(scope, receive, send)` |
| Suporta `async/await` | Não | Sim |
| WebSockets / SSE | Não | Sim |
| Servidores | Gunicorn, uWSGI, `wsgiref` | Uvicorn, Hypercorn, Daphne |
| Frameworks | Flask, Django (clássico) | FastAPI, Starlette, Django (async) |

**Arquivos**
- [`app_wsgi.py`](app_wsgi.py): aplicação WSGI "crua" usando só a biblioteca padrão.
- [`app_asgi.py`](app_asgi.py): aplicação ASGI "crua" (é isto que o FastAPI esconde de você).
- [`app_fastapi.py`](app_fastapi.py): a mesma resposta em FastAPI (que **é** uma aplicação ASGI).

## Como rodar
```powershell
python app_wsgi.py                      # servidor WSGI da stdlib na porta 8001
uvicorn app_asgi:app --port 8002        # ASGI cru
uvicorn app_fastapi:app --port 8003     # FastAPI
```
Em cada um, abra `http://127.0.0.1:<porta>/` no navegador. Para parar: `Ctrl+C`.

## Roteiro de gravação
1. Mostrar o WSGI (poucas linhas) e explicar `environ` e `start_response`.
2. Mostrar o ASGI (`scope`, `receive`, `send`) e por que ele permite `await`.
3. `uvicorn app_asgi:app` e depois `uvicorn app_fastapi:app`: o FastAPI é só uma app ASGI mais completa.
4. Conectar com a aula anterior: o event loop vive dentro do Uvicorn.
5. Em produção: `gunicorn -k uvicorn.workers.UvicornWorker app.main:app` (vários workers).
