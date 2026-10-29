# Videoaula 1 — O padrão OpenAPI e por que escolhemos o FastAPI (10 min)

**Objetivo:** criar a primeira API, abrir a documentação automática e entender o contrato OpenAPI.

**Arquivos**
- [`main.py`](main.py): API mínima com 3 rotas e metadados para o Swagger.

## Como rodar (dentro desta pasta, com o ambiente ativo)
```powershell
pip install fastapi "uvicorn[standard]"
uvicorn main:app --reload
```
Abrir: <http://127.0.0.1:8000/docs> (Swagger UI), <http://127.0.0.1:8000/redoc> e <http://127.0.0.1:8000/openapi.json>.

## Roteiro de gravação
1. O que é uma API e o que é um *contrato* (OpenAPI/Swagger): descreve rotas, parâmetros e respostas em JSON.
2. Subir o `main.py` e testar a rota `/` no navegador.
3. Mostrar o Swagger UI e usar o botão **Try it out**.
4. Abrir `/openapi.json` e relacionar cada trecho com o que aparece no Swagger.
5. Por que FastAPI: type hints viram validação + documentação, async nativo, desempenho.
