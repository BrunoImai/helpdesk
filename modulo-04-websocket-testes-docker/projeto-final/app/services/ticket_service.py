"""Regras de negócio dos chamados, agora persistidos no MongoDB com Beanie."""

from datetime import UTC, datetime

from beanie import PydanticObjectId
from beanie.operators import Push

from app.models.ticket import Mensagem, Ticket
from app.schemas.enums import Prioridade, StatusChamado
from app.schemas.ticket import ResumoStatus, TicketCreate


class TicketNotFoundError(Exception):
    """Levantada quando um chamado não existe."""

    def __init__(self, ticket_id: PydanticObjectId) -> None:
        self.ticket_id = ticket_id
        super().__init__(f"Chamado {ticket_id} não encontrado")


class TicketService:
    async def criar(self, dados: TicketCreate) -> Ticket:
        ticket = Ticket(**dados.model_dump())
        return await ticket.insert()

    async def listar(
        self,
        status: StatusChamado | None = None,
        prioridade: Prioridade | None = None,
        skip: int = 0,
        limit: int = 10,
    ) -> list[Ticket]:
        filtros: dict[str, object] = {}
        if status is not None:
            filtros["status"] = status.value
        if prioridade is not None:
            filtros["prioridade"] = prioridade.value
        return (
            await Ticket.find(filtros)
            .sort("-criado_em")
            .skip(skip)
            .limit(limit)
            .to_list()
        )

    async def listar_resolvidos(self) -> list[Ticket]:
        """Só os chamados com status 'resolvido' (Avaliação da Aula 3)."""
        return (
            await Ticket.find(Ticket.status == StatusChamado.RESOLVIDO)
            .sort("-criado_em")
            .to_list()
        )

    async def buscar(self, ticket_id: PydanticObjectId) -> Ticket:
        ticket = await Ticket.get(ticket_id)
        if ticket is None:
            raise TicketNotFoundError(ticket_id)
        return ticket

    async def substituir(
        self, ticket_id: PydanticObjectId, dados: TicketCreate
    ) -> Ticket:
        ticket = await self.buscar(ticket_id)
        campos = {**dados.model_dump(), "atualizado_em": datetime.now(UTC)}
        await ticket.set(campos)
        return ticket

    async def atualizar_status(
        self, ticket_id: PydanticObjectId, status: StatusChamado
    ) -> Ticket:
        ticket = await self.buscar(ticket_id)
        await ticket.set({"status": status, "atualizado_em": datetime.now(UTC)})
        return ticket

    async def adicionar_mensagem(
        self, ticket_id: PydanticObjectId, autor: str, texto: str
    ) -> Mensagem:
        """Guarda uma mensagem do chat no histórico do chamado ($push no MongoDB)."""
        ticket = await self.buscar(ticket_id)
        mensagem = Mensagem(autor=autor, texto=texto)
        await ticket.update(Push({Ticket.mensagens: mensagem}))
        return mensagem

    async def remover(self, ticket_id: PydanticObjectId) -> None:
        ticket = await self.buscar(ticket_id)
        await ticket.delete()

    async def resumo_por_status(self) -> list[ResumoStatus]:
        """Agregação: quantos chamados existem em cada status."""
        pipeline = [
            {"$group": {"_id": "$status", "total": {"$sum": 1}}},
            {"$sort": {"total": -1}},
        ]
        resultado = await Ticket.aggregate(pipeline).to_list()
        return [
            ResumoStatus(status=item["_id"], total=item["total"]) for item in resultado
        ]
