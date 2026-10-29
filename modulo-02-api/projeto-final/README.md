# HelpDesk — Projeto final do Módulo 2

API REST do HelpDesk com FastAPI: rotas assíncronas, camadas Router/Service, injeção de dependências,
erros humanizados, tarefas de fundo e documentação automática (Swagger). Os dados ficam **em memória**
(somem ao reiniciar). No Módulo 3 a camada `services/` passa a usar o MongoDB.

```
app/
  main.py                    # cria o FastAPI, trata erros, inclui routers
  dependencies.py            # Depends: serviço e paginação
  routers/tickets.py         # endpoints HTTP (camada Router)
  services/ticket_service.py # regras de negócio (camada Service)
  services/email_service.py  # e-mail simulado (BackgroundTasks)
  schemas/                   # contratos Pydantic (TicketCreate, TicketOut...)
  core/config.py             # configurações (.env)
```

## Como rodar
```powershell
cd modulo-02-api\projeto-final
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```
- Swagger: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>
- OpenAPI (JSON): <http://127.0.0.1:8000/openapi.json>

Teste rápido sem abrir o navegador: `python smoke_test.py`.

## Endpoints
| Verbo | Rota | Descrição | Sucesso | Erros |
|---|---|---|---|---|
| POST | `/tickets` | Abre um chamado (e envia e-mail em segundo plano) | 201 | 422 |
| GET | `/tickets` | Lista com filtros `?status=&prioridade=&skip=&limit=` | 200 | 422 |
| GET | `/tickets/{id}` | Consulta um chamado | 200 | 404 |
| PUT | `/tickets/{id}` | Substitui os dados | 200 | 404, 422 |
| PATCH | `/tickets/{id}/status` | Altera apenas o status | 200 | 404, 422 |
| DELETE | `/tickets/{id}` | Apaga | 204 | 404 |

## Desafio hands-on do Módulo 2 (checklist)
- [x] Rotas de criar e listar chamados assíncronas (`async def`)
- [x] Erro "Chamado não encontrado" tratado com mensagem humanizada (404)
- [x] Tudo documentado no Swagger (`summary`, `tags`, `responses`)
