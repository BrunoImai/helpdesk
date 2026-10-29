"""VIDEOAULA 2 — Camada Service: regras de negócio e armazenamento.

Repare: nada aqui importa `fastapi`. Esta camada não sabe o que é HTTP.
"""

from schemas import TicketCreate, TicketOut

_tickets: dict[int, TicketOut] = {}
_proximo_id = 1


def criar_ticket(dados: TicketCreate) -> TicketOut:
    global _proximo_id
    ticket = TicketOut(id=_proximo_id, **dados.model_dump())
    _tickets[ticket.id] = ticket
    _proximo_id += 1
    return ticket


def listar_tickets() -> list[TicketOut]:
    return list(_tickets.values())


def buscar_ticket(ticket_id: int) -> TicketOut | None:
    return _tickets.get(ticket_id)
