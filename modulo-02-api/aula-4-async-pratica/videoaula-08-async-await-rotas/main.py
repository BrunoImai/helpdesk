"""
VIDEOAULA 8 — async/await nas rotas.

Execute:  uvicorn main:app --reload
"""

import asyncio
import time

from fastapi import FastAPI

app = FastAPI(title="HelpDesk API — Videoaula 8")


# >>> DEMONSTRAÇÃO 1: CERTO — async def + await (não bloqueia o event loop)
@app.get("/async", tags=["Demo"])
async def rota_async() -> dict[str, str]:
    await asyncio.sleep(1)  # imagine: await colecao.find().to_list()
    return {"rota": "async", "resultado": "ok"}


# >>> DEMONSTRAÇÃO 2: CERTO — def comum com código bloqueante
#     O FastAPI executa rotas `def` em um pool de threads, então o loop continua livre.
@app.get("/sync", tags=["Demo"])
def rota_sync() -> dict[str, str]:
    time.sleep(1)
    return {"rota": "sync", "resultado": "ok"}


# >>> DEMONSTRAÇÃO 3: ERRADO — async def com código bloqueante
#     Congela o event loop: nenhuma outra requisição é atendida durante o sleep.
@app.get("/async-bloqueante", tags=["Demo"])
async def rota_async_bloqueante() -> dict[str, str]:
    time.sleep(1)
    return {"rota": "async-bloqueante", "resultado": "ok (mas travou o servidor)"}
