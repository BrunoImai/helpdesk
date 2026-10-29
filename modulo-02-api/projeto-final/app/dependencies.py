"""Dependências compartilhadas entre os routers (injeção com `Depends`)."""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends, Query

from app.services.ticket_service import TicketService


@lru_cache
def get_ticket_service() -> TicketService:
    """Uma única instância do serviço durante a vida da aplicação."""
    return TicketService()


TicketServiceDep = Annotated[TicketService, Depends(get_ticket_service)]


class Paginacao:
    """Parâmetros de paginação reutilizáveis (?skip=0&limit=10)."""

    def __init__(
        self,
        skip: Annotated[int, Query(ge=0, description="Quantos itens pular")] = 0,
        limit: Annotated[int, Query(ge=1, le=100, description="Máximo de itens")] = 10,
    ) -> None:
        self.skip = skip
        self.limit = limit


PaginacaoDep = Annotated[Paginacao, Depends()]
