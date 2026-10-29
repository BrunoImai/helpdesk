# Videoaula 10 — Exigindo o "crachá" (`Depends`) em rotas exclusivas para suporte (12 min)

**Objetivo:** criar a dependência `get_agente_atual` e usá-la para trancar rotas.

| Rota | Acesso |
|---|---|
| `POST /auth/login` | público |
| `POST /tickets` | público (o cliente abre o chamado) |
| `GET /tickets` | **token** |
| `PATCH /tickets/{id}/status` | **token** |
| `DELETE /tickets/{id}` | **token** |
| `GET /auth/eu` | **token** |

**Arquivos novos/alterados:** [`dependencies.py`](dependencies.py) e [`main.py`](main.py). Os demais vêm da Videoaula 9.

## Como rodar
```powershell
pip install -r requirements.txt
copy .env.example .env
python criar_agente.py "Ana Souza" ana@helpdesk.com      # se ainda não criou
uvicorn main:app --reload
```
Teste no Swagger: `GET /tickets` sem login (**401**) -> **Authorize** -> `GET /tickets` (**200**).
Com `curl`:
```powershell
curl -X POST http://127.0.0.1:8000/auth/login -d "username=ana@helpdesk.com&password=SUA_SENHA"
curl http://127.0.0.1:8000/tickets -H "Authorization: Bearer <TOKEN>"
```

## Roteiro de gravação
1. `OAuth2PasswordBearer`: extrai o token do cabeçalho `Authorization` e habilita o botão **Authorize**.
2. `get_agente_atual`: decodifica o token, busca o atendente e responde **401** se algo falhar.
3. Duas formas de usar: `agente: AgenteAtual` (quando preciso dos dados) e `dependencies=[Depends(...)]` (só para bloquear).
4. Testar: sem token (401), token inválido (401), token expirado (401), token válido (200).
5. Diferença entre **401** (quem é você?) e **403** (você não tem permissão), citar para o aluno.
