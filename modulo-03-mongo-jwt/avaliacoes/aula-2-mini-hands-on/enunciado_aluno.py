"""
AVALIAÇÃO DA AULA 2 — Mini Hands-on (ENUNCIADO)

1. Copie `.env.example` para `.env` e preencha `MONGO_URI` com a connection string fornecida.
2. Complete a função `init_db()` abaixo para conectar ao MongoDB com Motor
   e registrar o modelo `Ticket` no Beanie.
3. Chame `init_db()` no `lifespan` do FastAPI.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from config import get_settings
from fastapi import FastAPI
from models import Ticket  # noqa: F401


async def init_db() -> object:
    settings = get_settings()  # noqa: F841
    # TODO 1: crie o cliente Motor com `settings.mongo_uri`
    # TODO 2: chame `await init_beanie(database=..., document_models=[Ticket])`
    # TODO 3: devolva o cliente
    raise NotImplementedError


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # TODO 4: chame init_db() aqui e feche o cliente depois do `yield`
    yield


app = FastAPI(lifespan=lifespan)
