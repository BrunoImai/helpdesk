# Videoaula 8 — Usando `async/await` nas rotas do HelpDesk (12 min)

**Objetivo:** escolher entre `def` e `async def` corretamente e ver o efeito disso com 5 requisições simultâneas.

**Arquivos**
- [`main.py`](main.py): três rotas que simulam uma consulta lenta ao banco (1 s) de formas diferentes.
- [`medir_concorrencia.py`](medir_concorrencia.py): dispara 5 requisições ao mesmo tempo e mede o tempo total.

| Rota | Código | Tempo para 5 requisições simultâneas |
|---|---|---|
| `/async` | `async def` + `await asyncio.sleep(1)` | ~1 s |
| `/sync` | `def` + `time.sleep(1)` (FastAPI usa um *threadpool*) | ~1 s |
| `/async-bloqueante` | `async def` + `time.sleep(1)` (ERRADO) | ~5 s |

## Como rodar
```powershell
pip install fastapi "uvicorn[standard]" httpx
python medir_concorrencia.py          # mede sem precisar subir servidor
uvicorn main:app --reload             # para testar no Swagger
```

## Roteiro de gravação
1. Regra de ouro: se dentro da rota você usa `await`, a rota é `async def`.
2. Se usa uma biblioteca **bloqueante** (ex.: `requests`, `time.sleep`), use `def` (o FastAPI roda em thread).
3. Rodar `medir_concorrencia.py` e comentar os 3 resultados.
4. Mostrar a versão errada (`/async-bloqueante`): o servidor inteiro "congela".
5. Aplicar no HelpDesk: `projeto-final/app/routers/tickets.py` já usa `async def` + `await service...`.
