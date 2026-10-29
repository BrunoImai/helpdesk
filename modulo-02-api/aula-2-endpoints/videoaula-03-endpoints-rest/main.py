"""
VIDEOAULA 3 — CRUD semântico do HelpDesk (dados em memória).

Execute:  uvicorn main:app --reload
"""

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="HelpDesk API — Videoaula 3")


class TicketCreate(BaseModel):
    titulo: str = Field(min_length=5, max_length=100)
    descricao: str = Field(min_length=10)
    email_solicitante: EmailStr


class Ticket(TicketCreate):
    id: int
    status: str = "aberto"


BANCO: dict[int, Ticket] = {}
proximo_id = 1


# GET: lê dados (não altera nada)
@app.get("/tickets", response_model=list[Ticket], tags=["Chamados"])
def listar() -> list[Ticket]:
    return list(BANCO.values())


@app.get("/tickets/{ticket_id}", response_model=Ticket, tags=["Chamados"])
def obter(ticket_id: int) -> Ticket:
    if ticket_id not in BANCO:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    return BANCO[ticket_id]


# POST: cria um recurso novo -> 201 Created
@app.post(
    "/tickets",
    response_model=Ticket,
    status_code=status.HTTP_201_CREATED,
    tags=["Chamados"],
)
def criar(dados: TicketCreate) -> Ticket:
    global proximo_id
    ticket = Ticket(id=proximo_id, **dados.model_dump())
    BANCO[ticket.id] = ticket
    proximo_id += 1
    return ticket


# PUT: substitui o recurso inteiro
@app.put("/tickets/{ticket_id}", response_model=Ticket, tags=["Chamados"])
def substituir(ticket_id: int, dados: TicketCreate) -> Ticket:
    if ticket_id not in BANCO:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    BANCO[ticket_id] = Ticket(
        id=ticket_id, status=BANCO[ticket_id].status, **dados.model_dump()
    )
    return BANCO[ticket_id]


# DELETE: remove -> 204 No Content (sem corpo)
@app.delete(
    "/tickets/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Chamados"]
)
def apagar(ticket_id: int) -> Response:
    if ticket_id not in BANCO:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    del BANCO[ticket_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
