"""
AVALIAÇÃO DA AULA 3 — Mini Hands-on (ENUNCIADO)

Crie uma NOVA rota `GET /tickets/resolvidos` que liste exclusivamente os chamados
com status "resolvido". Use uma query do Beanie (`Ticket.find(...)`).

Dicas:
- O campo é `Ticket.status` e o valor é `StatusChamado.RESOLVIDO`.
- Lembre-se do `await` e do `.to_list()`.
- Converta cada documento com `TicketOut.model_validate(...)`.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from database import init_db
from fastapi import FastAPI
from models import StatusChamado, Ticket  # noqa: F401
from schemas import TicketOut  # noqa: F401


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    client = await init_db()
    yield
    client.close()


app = FastAPI(lifespan=lifespan)

# TODO: escreva a rota GET /tickets/resolvidos aqui
