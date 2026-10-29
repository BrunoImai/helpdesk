"""VIDEOAULA 3 — Conexão com o MongoDB (Motor) e inicialização do Beanie."""

from beanie import init_beanie
from config import get_settings
from models import Ticket
from motor.motor_asyncio import AsyncIOMotorClient


async def init_db() -> AsyncIOMotorClient:
    settings = get_settings()

    # 1. Motor: o driver assíncrono do MongoDB
    client = AsyncIOMotorClient(settings.mongo_uri, serverSelectionTimeoutMS=5000)

    # 2. Beanie: o ODM que transforma coleções em classes Python (Document)
    await init_beanie(
        database=client[settings.mongo_db_name],
        document_models=[Ticket],
    )
    return client
