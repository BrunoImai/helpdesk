"""VIDEOAULA 2 — Camada Router: só traduz HTTP <-> Service."""

from fastapi import APIRouter, HTTPException, status
from schemas import TicketCreate, TicketOut
from services import ticket_service

router = APIRouter(prefix="/tickets", tags=["Chamados"])


@router.post("", response_model=TicketOut, status_code=status.HTTP_201_CREATED)
def criar(dados: TicketCreate) -> TicketOut:
    return ticket_service.criar_ticket(dados)


@router.get("", response_model=list[TicketOut])
def listar() -> list[TicketOut]:
    return ticket_service.listar_tickets()


@router.get("/{ticket_id}", response_model=TicketOut)
def obter(ticket_id: int) -> TicketOut:
    ticket = ticket_service.buscar_ticket(ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    return ticket
