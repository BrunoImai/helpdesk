"""
VIDEOAULA 7 — O FastAPI é uma aplicação ASGI com muitos recursos prontos.

Execute:  uvicorn app_fastapi:app --port 8003   e abra http://127.0.0.1:8003/
"""

import asyncio

from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/{caminho:path}")
async def qualquer(caminho: str, request: Request) -> dict[str, str]:
    await asyncio.sleep(0.1)
    return {"servidor": "ASGI (FastAPI)", "caminho": request.url.path}
