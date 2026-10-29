"""Endpoints REST de chamados (camada Router: só HTTP, sem regra de negócio)."""

from typing import Annotated, Any

from fastapi import APIRouter, BackgroundTasks, Path, Query, Response, status

from app.dependencies import PaginacaoDep, TicketServiceDep
from app.schemas.enums import Prioridade, StatusChamado
from app.schemas.ticket import TicketCreate, TicketOut, TicketStatusUpdate
from app.services.email_service import enviar_email_confirmacao

router = APIRouter(prefix="/tickets", tags=["Chamados"])

TicketId = Annotated[int, Path(ge=1, description="Número do chamado")]

RESPOSTA_404: dict[int | str, dict[str, Any]] = {
    404: {"description": "Chamado não encontrado"}
}


@router.post(
    "",
    response_model=TicketOut,
    status_code=status.HTTP_201_CREATED,
    summary="Abrir um chamado",
)
async def criar_ticket(
    dados: TicketCreate,
    service: TicketServiceDep,
    background_tasks: BackgroundTasks,
) -> TicketOut:
    ticket = await service.criar(dados)
    # O e-mail é enviado DEPOIS de responder: o cliente não espera por ele.
    background_tasks.add_task(
        enviar_email_confirmacao, ticket.email_solicitante, ticket.id
    )
    return ticket


@router.get("", response_model=list[TicketOut], summary="Listar a fila de chamados")
async def listar_tickets(
    service: TicketServiceDep,
    paginacao: PaginacaoDep,
    status_: Annotated[
        StatusChamado | None, Query(alias="status", description="Filtrar por status")
    ] = None,
    prioridade: Annotated[
        Prioridade | None, Query(description="Filtrar por prioridade")
    ] = None,
) -> list[TicketOut]:
    return await service.listar(
        status=status_,
        prioridade=prioridade,
        skip=paginacao.skip,
        limit=paginacao.limit,
    )


@router.get(
    "/{ticket_id}",
    response_model=TicketOut,
    responses=RESPOSTA_404,
    summary="Consultar um chamado",
)
async def obter_ticket(ticket_id: TicketId, service: TicketServiceDep) -> TicketOut:
    return await service.buscar(ticket_id)


@router.put(
    "/{ticket_id}",
    response_model=TicketOut,
    responses=RESPOSTA_404,
    summary="Substituir os dados de um chamado",
)
async def substituir_ticket(
    ticket_id: TicketId, dados: TicketCreate, service: TicketServiceDep
) -> TicketOut:
    return await service.substituir(ticket_id, dados)


@router.patch(
    "/{ticket_id}/status",
    response_model=TicketOut,
    responses=RESPOSTA_404,
    summary="Alterar o status de um chamado",
)
async def alterar_status(
    ticket_id: TicketId, dados: TicketStatusUpdate, service: TicketServiceDep
) -> TicketOut:
    return await service.atualizar_status(ticket_id, dados.status)


@router.delete(
    "/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=RESPOSTA_404,
    summary="Apagar um chamado",
)
async def apagar_ticket(ticket_id: TicketId, service: TicketServiceDep) -> Response:
    await service.remover(ticket_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
