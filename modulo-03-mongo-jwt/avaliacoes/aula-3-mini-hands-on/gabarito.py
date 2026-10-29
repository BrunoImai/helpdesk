"""
AVALIAÇÃO DA AULA 3 — Mini Hands-on (GABARITO)

Rota que lista EXCLUSIVAMENTE os chamados com status "resolvido".

Execute:  uvicorn gabarito:app --reload     e abra  GET /tickets/resolvidos
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from database import init_db
from fastapi import FastAPI
from models import StatusChamado, Ticket
from schemas import TicketOut


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    client = await init_db()
    yield
    client.close()


app = FastAPI(lifespan=lifespan)


@app.get("/tickets/resolvidos", response_model=list[TicketOut])
async def listar_resolvidos() -> list[TicketOut]:
    # A query do Beanie: filtra pelo campo `status` e ordena do mais novo ao mais antigo
    tickets = (
        await Ticket.find(Ticket.status == StatusChamado.RESOLVIDO)
        .sort("-criado_em")
        .to_list()
    )
    return [TicketOut.model_validate(t) for t in tickets]
