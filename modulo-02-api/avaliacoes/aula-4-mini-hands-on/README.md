# Avaliação da Aula 4 — Mini Hands-on (gabarito)

**Desafio do aluno:** transformar uma rota de listagem de chamados escrita de forma **síncrona** em **assíncrona**
com `async def` e disparar uma tarefa de fundo via `BackgroundTasks`.

- [`enunciado_aluno.py`](enunciado_aluno.py): ponto de partida (rota síncrona).
- [`gabarito.py`](gabarito.py): solução esperada.

## Como rodar
```powershell
pip install fastapi "uvicorn[standard]" httpx
uvicorn gabarito:app --reload
```
No Swagger, chame `GET /tickets`: a resposta vem na hora e o log mostra "Registrando acesso..." logo depois.

## Critérios de correção
| # | Critério |
|---|---|
| 1 | A rota usa `async def` |
| 2 | A espera simulada usa `await asyncio.sleep(...)` (e não `time.sleep`) |
| 3 | `BackgroundTasks` é recebido como parâmetro da rota |
| 4 | `background_tasks.add_task(registrar_acesso, ...)` é chamado |
| 5 | A resposta continua devolvendo a lista de chamados |
