# Avaliação da Aula 3 — Mini Hands-on (gabarito)

**Desafio do aluno:** escrever um teste simples que verifique o erro **401 Unauthorized** ao acessar uma rota
protegida sem enviar token.

- [`enunciado_aluno.py`](enunciado_aluno.py): ponto de partida (falha com `NotImplementedError` até ser completado).
- [`gabarito.py`](gabarito.py): solução esperada.

## Como rodar
```powershell
# a partir da pasta da avaliação, com o ambiente virtual do projeto-final ativo
pip install -r ..\..\projeto-final\requirements-dev.txt
pytest gabarito.py -v
```
Não precisa de MongoDB nem de Docker.

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
requisição antes de tocar no Beanie/MongoDB. Se o teste fosse de uma rota **liberada**, aí sim precisaria do
banco (falso) — veja `projeto-final/tests/conftest.py`.
