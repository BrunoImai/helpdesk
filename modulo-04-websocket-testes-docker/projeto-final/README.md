# HelpDesk — Projeto final do Módulo 4

O HelpDesk completo: **API REST** + **MongoDB** + **JWT** + **chat em tempo real (WebSocket)** + **suíte de testes
verde no Pytest** + **empacotado com Docker**.

```
app/
  main.py                     # FastAPI, lifespan, routers
  routers/tickets.py          # CRUD de chamados (rotas do suporte protegidas)
  routers/auth.py             # login JWT
  routers/chat.py             # WebSocket /ws/tickets/{id} e página /chat
  services/chat_manager.py    # ConnectionManager (salas por chamado)
  services/ticket_service.py  # regras de negócio + adicionar_mensagem (chat)
  static/chat.html            # cliente web do chat
  ...                         # core/, models/, schemas/ (como no Módulo 3)
tests/
  unit/                       # testes de unidade (rápidos, sem I/O)
  api/                        # testes de integração com TestClient + MongoDB falso
  conftest.py                 # fixtures (client, agente, token...)
Dockerfile  .dockerignore  docker-compose.yml
```

## 1) Rodando os testes (não precisa de Mongo nem Docker)
```powershell
cd modulo-04-websocket-testes-docker\projeto-final
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pytest                      # tudo
pytest tests/unit           # só unidade
pytest -k chat -v           # só os testes do chat
```
Resultado esperado: **71 passed**.

## 2) Rodando a API sem Docker
```powershell
copy .env.example .env      # ajuste MONGO_URI e gere a SECRET_KEY
uvicorn app.main:app --reload
```
- Swagger: <http://127.0.0.1:8000/docs>
- Chat de teste no navegador: <http://127.0.0.1:8000/chat>

## 3) Rodando tudo com Docker
```powershell
copy .env.example .env      # defina ao menos SECRET_KEY
docker compose up --build
# em outro terminal, crie um atendente dentro do container:
docker compose exec api python -m scripts.criar_agente "Ana Souza" ana@helpdesk.com
```
Abra <http://127.0.0.1:8000/docs>. Para parar: `docker compose down` (os dados ficam no volume `mongo_data`).

## O chat (WebSocket)
| Quem | URL de conexão |
|---|---|
| Cliente | `ws://127.0.0.1:8000/ws/tickets/{ticket_id}?email=<e-mail do chamado>` |
| Suporte | `ws://127.0.0.1:8000/ws/tickets/{ticket_id}?token=<JWT do /auth/login>` |

1. Abra um chamado (`POST /tickets`) e copie o `id`.
2. Faça login (`POST /auth/login`) e copie o `access_token`.
3. Abra `/chat` em **duas abas**: uma como cliente (e-mail do chamado) e outra como suporte (token).
4. Troque mensagens. Elas ficam salvas no chamado (`GET /tickets/{id}` mostra o histórico).

## Desafio hands-on final do Módulo 4 (checklist)
- [x] Chat em tempo real via WebSocket integrado ao chamado
- [x] Suíte de testes passando verde no Pytest
- [x] API empacotada em Docker (`Dockerfile`) e orquestrada com `docker-compose.yml`

## Observações
- O `ConnectionManager` guarda as conexões **na memória de um processo**. Com vários workers/servidores, use um
  intermediário (ex.: Redis Pub/Sub). Veja a Videoaula 8.
- No chat, o cliente se identifica pelo e-mail do chamado (suficiente para estudo). Em produção, envie um link
  com token próprio para o cliente.
