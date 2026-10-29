"""
VIDEOAULA 4 — Salvando o primeiro chamado real no banco e listando a fila.

Execute:  uvicorn main:app --reload
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from database import init_db
from fastapi import FastAPI, status
from models import Ticket
from schemas import TicketCreate, TicketOut


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    client = await init_db()
    yield
    client.close()


app = FastAPI(title="HelpDesk API — Videoaula 4", lifespan=lifespan)


# >>> DEMONSTRAÇÃO 1: CREATE — transforma o JSON validado em um documento e salva
@app.post(
    "/tickets",
    response_model=TicketOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Chamados"],
)
async def criar_ticket(dados: TicketCreate) -> TicketOut:
    ticket = Ticket(**dados.model_dump())  # 1. monta o documento
    await ticket.insert()  # 2. grava no MongoDB (gera o _id)
    return TicketOut.model_validate(ticket)  # 3. devolve (id vira texto)


# >>> DEMONSTRAÇÃO 2: READ — lista a fila, do mais novo para o mais antigo
@app.get("/tickets", response_model=list[TicketOut], tags=["Chamados"])
async def listar_tickets() -> list[TicketOut]:
    tickets = await Ticket.find_all().sort("-criado_em").to_list()
    return [TicketOut.model_validate(t) for t in tickets]
