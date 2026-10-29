"""
VIDEOAULA 5 — CRUD completo: atualizando status e deletando chamados.

Execute:  uvicorn main:app --reload
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import UTC, datetime

from beanie import PydanticObjectId
from database import init_db
from fastapi import FastAPI, HTTPException, Response, status
from models import Ticket
from schemas import TicketCreate, TicketOut, TicketStatusUpdate


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    client = await init_db()
    yield
    client.close()


app = FastAPI(title="HelpDesk API — Videoaula 5", lifespan=lifespan)


async def buscar_ou_404(ticket_id: PydanticObjectId) -> Ticket:
    ticket = await Ticket.get(ticket_id)  # busca pelo _id
    if ticket is None:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    return ticket


# CREATE e READ (já vistos na Videoaula 4)
@app.post(
    "/tickets",
    response_model=TicketOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Chamados"],
)
async def criar_ticket(dados: TicketCreate) -> TicketOut:
    ticket = await Ticket(**dados.model_dump()).insert()
    return TicketOut.model_validate(ticket)


@app.get("/tickets", response_model=list[TicketOut], tags=["Chamados"])
async def listar_tickets() -> list[TicketOut]:
    tickets = await Ticket.find_all().sort("-criado_em").to_list()
    return [TicketOut.model_validate(t) for t in tickets]


# >>> DEMONSTRAÇÃO 1: READ de um só documento
@app.get("/tickets/{ticket_id}", response_model=TicketOut, tags=["Chamados"])
async def obter_ticket(ticket_id: PydanticObjectId) -> TicketOut:
    return TicketOut.model_validate(await buscar_ou_404(ticket_id))


# >>> DEMONSTRAÇÃO 2: UPDATE parcial com `set` ($set do MongoDB)
@app.patch("/tickets/{ticket_id}/status", response_model=TicketOut, tags=["Chamados"])
async def alterar_status(
    ticket_id: PydanticObjectId, dados: TicketStatusUpdate
) -> TicketOut:
    ticket = await buscar_ou_404(ticket_id)
    await ticket.set({"status": dados.status, "atualizado_em": datetime.now(UTC)})
    return TicketOut.model_validate(ticket)


# >>> DEMONSTRAÇÃO 3: UPDATE completo (substitui os campos enviados)
@app.put("/tickets/{ticket_id}", response_model=TicketOut, tags=["Chamados"])
async def substituir_ticket(
    ticket_id: PydanticObjectId, dados: TicketCreate
) -> TicketOut:
    ticket = await buscar_ou_404(ticket_id)
    await ticket.set({**dados.model_dump(), "atualizado_em": datetime.now(UTC)})
    return TicketOut.model_validate(ticket)


# >>> DEMONSTRAÇÃO 4: DELETE
@app.delete(
    "/tickets/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Chamados"],
)
async def apagar_ticket(ticket_id: PydanticObjectId) -> Response:
    ticket = await buscar_ou_404(ticket_id)
    await ticket.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
