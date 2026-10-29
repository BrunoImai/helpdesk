"""
VIDEOAULA 3 — Conectando o FastAPI ao MongoDB com Motor e Beanie.

Execute:  uvicorn main:app --reload
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from database import init_db
from fastapi import FastAPI
from models import Ticket


# >>> DEMONSTRAÇÃO: o lifespan roda UMA vez ao ligar e UMA vez ao desligar a API
@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    client = await init_db()  # conecta e registra os modelos
    yield  # <- a API fica atendendo requisições aqui
    client.close()  # fecha a conexão ao desligar


app = FastAPI(title="HelpDesk API — Videoaula 3", lifespan=lifespan)


@app.get("/")
async def raiz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/total-de-chamados")
async def total_de_chamados() -> dict[str, int]:
    """Prova que a conexão funciona: conta os documentos da coleção `tickets`."""
    return {"total": await Ticket.count()}
