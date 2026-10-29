# HelpDesk — Projeto final do Módulo 3

API do HelpDesk agora com **MongoDB** (Motor + Beanie) e **autenticação JWT** para as rotas do suporte.

```
app/
  main.py                    # FastAPI + lifespan (conecta no banco ao ligar)
  core/config.py             # Settings (.env): Mongo, SECRET_KEY, JWT
  core/database.py           # Motor + init_beanie
  core/security.py           # hash bcrypt + criar/decodificar JWT
  models/ticket.py           # Ticket (Document) + Mensagem embutida
  models/agente.py           # Agente (Document), e-mail único
  schemas/                   # contratos Pydantic (entrada/saída)
  services/ticket_service.py # CRUD, filtros e agregação (Beanie)
  services/agente_service.py # cadastro e autenticação
  dependencies.py            # Depends: serviço, paginação, get_agente_atual
  routers/tickets.py         # endpoints de chamados
  routers/auth.py            # /auth/login e /auth/eu
scripts/criar_agente.py      # cria um atendente no banco
smoke_test.py                # percorre a API inteira com um Mongo FALSO (sem instalar nada)
```

## Como rodar
```powershell
cd modulo-03-mongo-jwt\projeto-final
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```
1. Edite o `.env`:
   - `MONGO_URI`: use o Mongo local (`docker run -d -p 27017:27017 mongo:7`) **ou** a connection string do MongoDB Atlas (guia na Videoaula 3).
   - `SECRET_KEY`: gere com `python -c "import secrets; print(secrets.token_hex(32))"`.
2. Crie um atendente: `python -m scripts.criar_agente "Ana Souza" ana@helpdesk.com`
3. Suba a API: `uvicorn app.main:app --reload`
4. Abra <http://127.0.0.1:8000/docs>, clique em **Authorize** e entre com o e-mail e a senha do atendente.

Sem Mongo à mão? `python smoke_test.py` roda todo o fluxo com um banco falso em memória.

## Endpoints
| Verbo | Rota | Acesso | Descrição |
|---|---|---|---|
| POST | `/auth/login` | público | Gera o token JWT (formulário `username` = e-mail, `password`) |
| GET | `/auth/eu` | token | Dados do atendente logado |
| POST | `/tickets` | público | Abre um chamado |
| GET | `/tickets` | token | Lista a fila (`?status=&prioridade=&skip=&limit=`) |
| GET | `/tickets/resolvidos` | token | Só os resolvidos |
| GET | `/tickets/resumo` | token | Agregação: total por status |
| GET | `/tickets/{id}` | token | Consulta um chamado |
| PUT | `/tickets/{id}` | token | Substitui os dados |
| PATCH | `/tickets/{id}/status` | token | Altera o status |
| DELETE | `/tickets/{id}` | token | Apaga |

## Desafio hands-on do Módulo 3 (checklist)
- [x] API conectada ao cluster MongoDB (`MONGO_URI` no `.env`)
- [x] CRUD completo persistido no banco
- [x] Rotas de edição de status (e demais rotas do suporte) trancadas com token JWT válido

## Segurança: lembretes
- Nunca versione o `.env`. Se uma senha/connection string vazar, **troque-a imediatamente**.
- O hash bcrypt é de mão única; o JWT é **assinado**, não criptografado: não coloque dados sensíveis no payload.
- Em produção use HTTPS, um `SECRET_KEY` longo e tokens com expiração curta.
