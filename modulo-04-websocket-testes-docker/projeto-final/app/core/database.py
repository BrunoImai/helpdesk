"""Conexão com o MongoDB (Motor) e inicialização do Beanie."""

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import get_settings
from app.models.agente import Agente
from app.models.ticket import Ticket

# Todos os modelos (coleções) que o Beanie deve conhecer
DOCUMENT_MODELS = [Ticket, Agente]


async def init_db(
    database: AsyncIOMotorDatabase | None = None,
) -> AsyncIOMotorClient | None:
    """Inicializa o Beanie.

    Em produção cria o cliente Motor a partir de `MONGO_URI`. Nos testes é possível
    passar um `database` pronto (ex.: um banco falso em memória).
    Devolve o cliente criado (para ser fechado no desligamento) ou None.
    """
    client: AsyncIOMotorClient | None = None
    if database is None:
        settings = get_settings()
        client = AsyncIOMotorClient(settings.mongo_uri, serverSelectionTimeoutMS=5000)
        database = client[settings.mongo_db_name]

    await init_beanie(database=database, document_models=DOCUMENT_MODELS)
    return client
