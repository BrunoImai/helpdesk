"""
AVALIAÇÃO DA AULA 2 — Mini Hands-on (GABARITO)

Execute:  uvicorn gabarito:app --reload     e abra  GET /total
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from beanie import init_beanie
from config import get_settings
from fastapi import FastAPI
from models import Ticket
from motor.motor_asyncio import AsyncIOMotorClient


async def init_db() -> AsyncIOMotorClient:
    settings = get_settings()
    client = AsyncIOMotorClient(settings.mongo_uri, serverSelectionTimeoutMS=5000)
    await init_beanie(
        database=client[settings.mongo_db_name],
        document_models=[Ticket],
    )
    return client


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    client = await init_db()
    yield
    client.close()


app = FastAPI(lifespan=lifespan)


@app.get("/total")
async def total() -> dict[str, int]:
    return {"total_de_chamados": await Ticket.count()}
