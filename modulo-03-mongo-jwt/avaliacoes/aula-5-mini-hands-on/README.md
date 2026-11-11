# Avaliação da Aula 5 — Mini Hands-on (gabarito)

**Desafio do aluno:** escrever um teste simples que verifique o erro **401 Unauthorized** ao acessar uma rota
protegida sem enviar token.

- [`enunciado_aluno.py`](enunciado_aluno.py): ponto de partida (falha com `NotImplementedError` até ser completado).
- [`gabarito.py`](gabarito.py): solução esperada.

## Como rodar
```powershell
# com o ambiente virtual do projeto-final ativo
cd modulo-03-mongo-jwt\avaliacoes\aula-5-mini-hands-on
pytest gabarito.py -v
```
Não precisa de MongoDB.

## Critérios de correção
| # | Critério |
|---|---|
| 1 | Usa `TestClient(app)` e chama uma rota protegida (`GET /tickets`) **sem** `Authorization` |
| 2 | Verifica `status_code == 401` |
| 3 | O teste passa **sem banco de dados** (a autenticação barra antes da consulta) |
| 4 | (Bônus) Verifica `WWW-Authenticate: Bearer` e/ou testa com token inválido |
| 5 | (Bônus) Usa `parametrize` para cobrir várias rotas |

## Para discutir
Por que o teste não precisou do lifespan (`with TestClient(...)`)? Porque a dependência de autenticação rejeita a
requisição antes de tocar no Beanie/MongoDB.
