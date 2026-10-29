"""Regras de negócio dos chamados (camada Service).

Neste módulo os dados ficam em memória. No Módulo 3 esta camada passa a
conversar com o MongoDB, sem que os routers precisem mudar.
"""

from app.schemas.enums import Prioridade, StatusChamado
from app.schemas.ticket import TicketCreate, TicketOut


class TicketNotFoundError(Exception):
    """Levantada quando um chamado não existe."""

    def __init__(self, ticket_id: int) -> None:
        self.ticket_id = ticket_id
        super().__init__(f"Chamado {ticket_id} não encontrado")


class TicketService:
    def __init__(self) -> None:
        self._tickets: dict[int, TicketOut] = {}
        self._proximo_id = 1

    async def criar(self, dados: TicketCreate) -> TicketOut:
        ticket = TicketOut(id=self._proximo_id, **dados.model_dump())
        self._tickets[ticket.id] = ticket
        self._proximo_id += 1
        return ticket

    async def listar(
        self,
        status: StatusChamado | None = None,
        prioridade: Prioridade | None = None,
        skip: int = 0,
        limit: int = 10,
    ) -> list[TicketOut]:
        tickets = list(self._tickets.values())
        if status is not None:
            tickets = [t for t in tickets if t.status == status]
        if prioridade is not None:
            tickets = [t for t in tickets if t.prioridade == prioridade]
        return tickets[skip : skip + limit]

    async def buscar(self, ticket_id: int) -> TicketOut:
        ticket = self._tickets.get(ticket_id)
        if ticket is None:
            raise TicketNotFoundError(ticket_id)
        return ticket

    async def substituir(self, ticket_id: int, dados: TicketCreate) -> TicketOut:
        atual = await self.buscar(ticket_id)
        novo = TicketOut(
            id=atual.id,
            status=atual.status,
            criado_em=atual.criado_em,
            **dados.model_dump(),
        )
        self._tickets[ticket_id] = novo
        return novo

    async def atualizar_status(
        self, ticket_id: int, status: StatusChamado
    ) -> TicketOut:
        atual = await self.buscar(ticket_id)
        atualizado = atual.model_copy(update={"status": status})
        self._tickets[ticket_id] = atualizado
        return atualizado

    async def remover(self, ticket_id: int) -> None:
        await self.buscar(ticket_id)
        del self._tickets[ticket_id]
