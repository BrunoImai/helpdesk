# Videoaula 7 — Testando erros e rotas autenticadas (12 min)

**Objetivo:** provar que a API **recusa** o que deve recusar (401, 404, 422) e **aceita** com token válido.

**Arquivo:** [`projeto/test_auth.py`](projeto/test_auth.py) (cópia de `projeto-final/tests/api/test_auth.py`;
usa as fixtures `client`, `agente`, `auth_headers` do `tests/conftest.py`).

## Como rodar
```powershell
cd ..\..\projeto-final
pytest tests/api/test_auth.py -v
```

## O que o arquivo cobre
| Cenário | Esperado |
|---|---|
| Login correto | 200 + `access_token` (JWT com 3 partes) |
| Senha errada **e** e-mail inexistente | 401 com a **mesma** resposta (não revela quais e-mails existem) |
| Rotas do suporte sem token | 401 + cabeçalho `WWW-Authenticate: Bearer` (`parametrize` em 7 rotas) |
| Token lixo / expirado / de atendente removido | 401 |
| `/auth/eu` com token válido | 200 e **nunca** devolve senha/hash |
| `POST /tickets` (rota pública) | 201 sem login |

## Técnicas para destacar
- `@pytest.mark.parametrize`: um teste, 7 rotas.
- Token expirado de propósito: `criar_token_acesso(email, expira_em=timedelta(seconds=-5))`.
- `pytest.raises` e checagem de **mensagem** de erro, não só do status.
- Fixture `auth_headers`: login real uma vez e reaproveita o cabeçalho `Authorization: Bearer ...`.

## Roteiro de gravação
1. Tabela "o que deveria acontecer" antes do código (testes nascem da especificação).
2. Login feliz e login infeliz.
3. `parametrize` das rotas protegidas; rodar com `-v` e mostrar os 7 casos.
4. Gerar um token expirado e ver o 401.
5. **Quebrar de propósito:** remover `Depends(get_agente_atual)` de uma rota e ver o teste vermelho.
