"""VIDEOAULA 10 — Conexão com o MongoDB."""

from beanie import init_beanie
from config import get_settings
from models import Agente, Ticket
from motor.motor_asyncio import AsyncIOMotorClient


async def init_db() -> AsyncIOMotorClient:
    settings = get_settings()
    client = AsyncIOMotorClient(settings.mongo_uri, serverSelectionTimeoutMS=5000)
    await init_beanie(
        database=client[settings.mongo_db_name],
        document_models=[Ticket, Agente],
    )
    return client
