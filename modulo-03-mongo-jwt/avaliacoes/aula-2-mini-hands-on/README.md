# Avaliação da Aula 2 — Mini Hands-on (gabarito)

**Desafio do aluno:** pegar a *connection string* fornecida, preenchê-la corretamente no arquivo `.env` e escrever a
função de inicialização do cliente MongoDB no FastAPI.

- [`enunciado_aluno.py`](enunciado_aluno.py): ponto de partida com `TODO`.
- [`gabarito.py`](gabarito.py): solução esperada.
- [`.env.example`](.env.example), [`config.py`](config.py), [`models.py`](models.py): arquivos de apoio.

## Como rodar o gabarito
```powershell
pip install -r requirements.txt
copy .env.example .env      # preencha MONGO_URI
uvicorn gabarito:app --reload
```
`GET /total` deve responder `{"total_de_chamados": 0}` (ou o número de documentos existentes).

## Critérios de correção
| # | Critério |
|---|---|
| 1 | O `.env` contém `MONGO_URI` com usuário e senha **corretos** e não foi enviado ao Git |
| 2 | Usa `AsyncIOMotorClient(settings.mongo_uri)` (a string vem das configurações, não está escrita no código) |
| 3 | Chama `await init_beanie(database=client[...], document_models=[Ticket])` |
| 4 | A inicialização acontece no `lifespan` e o cliente é fechado ao desligar |
