"""Endpoints REST de chamados.

- Abrir chamado (POST) é público: o cliente não tem login.
- Consultar a fila, editar e apagar exigem o token JWT de um atendente.
"""

from typing import Annotated, Any

from beanie import PydanticObjectId
from fastapi import APIRouter, BackgroundTasks, Depends, Query, Response, status

from app.dependencies import PaginacaoDep, TicketServiceDep, get_agente_atual
from app.schemas.enums import Prioridade, StatusChamado
from app.schemas.ticket import (
    ResumoStatus,
    TicketCreate,
    TicketOut,
    TicketStatusUpdate,
)
from app.services.email_service import enviar_email_confirmacao

router = APIRouter(prefix="/tickets", tags=["Chamados"])

# Aplicada nas rotas exclusivas do suporte: exige o "crachá" (token JWT)
SOMENTE_SUPORTE = [Depends(get_agente_atual)]

RESPOSTAS_SUPORTE: dict[int | str, dict[str, Any]] = {
    401: {"description": "Token ausente, inválido ou expirado"},
    404: {"description": "Chamado não encontrado"},
}


@router.post(
    "",
    response_model=TicketOut,
    status_code=status.HTTP_201_CREATED,
    summary="Abrir um chamado (público)",
)
async def criar_ticket(
    dados: TicketCreate,
    service: TicketServiceDep,
    background_tasks: BackgroundTasks,
) -> TicketOut:
    ticket = await service.criar(dados)
    background_tasks.add_task(
        enviar_email_confirmacao, ticket.email_solicitante, str(ticket.id)
    )
    return TicketOut.model_validate(ticket)


@router.get(
    "",
    response_model=list[TicketOut],
    dependencies=SOMENTE_SUPORTE,
    responses={401: RESPOSTAS_SUPORTE[401]},
    summary="Listar a fila de chamados",
)
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
    tickets = await service.listar(
        status=status_,
        prioridade=prioridade,
        skip=paginacao.skip,
        limit=paginacao.limit,
    )
    return [TicketOut.model_validate(t) for t in tickets]


# ATENÇÃO: rotas fixas (/resolvidos, /resumo) vêm ANTES de /{ticket_id}
@router.get(
    "/resolvidos",
    response_model=list[TicketOut],
    dependencies=SOMENTE_SUPORTE,
    responses={401: RESPOSTAS_SUPORTE[401]},
    summary="Listar apenas os chamados resolvidos",
)
async def listar_resolvidos(service: TicketServiceDep) -> list[TicketOut]:
    tickets = await service.listar_resolvidos()
    return [TicketOut.model_validate(t) for t in tickets]


@router.get(
    "/resumo",
    response_model=list[ResumoStatus],
    dependencies=SOMENTE_SUPORTE,
    responses={401: RESPOSTAS_SUPORTE[401]},
    summary="Quantidade de chamados por status (agregação)",
)
async def resumo_por_status(service: TicketServiceDep) -> list[ResumoStatus]:
    return await service.resumo_por_status()


@router.get(
    "/{ticket_id}",
    response_model=TicketOut,
    dependencies=SOMENTE_SUPORTE,
    responses=RESPOSTAS_SUPORTE,
    summary="Consultar um chamado",
)
async def obter_ticket(
    ticket_id: PydanticObjectId, service: TicketServiceDep
) -> TicketOut:
    return TicketOut.model_validate(await service.buscar(ticket_id))


@router.put(
    "/{ticket_id}",
    response_model=TicketOut,
    dependencies=SOMENTE_SUPORTE,
    responses=RESPOSTAS_SUPORTE,
    summary="Substituir os dados de um chamado",
)
async def substituir_ticket(
    ticket_id: PydanticObjectId, dados: TicketCreate, service: TicketServiceDep
) -> TicketOut:
    return TicketOut.model_validate(await service.substituir(ticket_id, dados))


@router.patch(
    "/{ticket_id}/status",
    response_model=TicketOut,
    dependencies=SOMENTE_SUPORTE,
    responses=RESPOSTAS_SUPORTE,
    summary="Alterar o status de um chamado",
)
async def alterar_status(
    ticket_id: PydanticObjectId,
    dados: TicketStatusUpdate,
    service: TicketServiceDep,
) -> TicketOut:
    return TicketOut.model_validate(
        await service.atualizar_status(ticket_id, dados.status)
    )


@router.delete(
    "/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=SOMENTE_SUPORTE,
    responses=RESPOSTAS_SUPORTE,
    summary="Apagar um chamado",
)
async def apagar_ticket(
    ticket_id: PydanticObjectId, service: TicketServiceDep
) -> Response:
    await service.remover(ticket_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
