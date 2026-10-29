"""
VIDEOAULA 6 — Filtros complexos e agregações.

Execute:  uvicorn main:app --reload
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import UTC, datetime, timedelta
from typing import Annotated

from beanie.operators import In, Or, RegEx
from database import init_db
from fastapi import FastAPI, Query, status
from models import Prioridade, StatusChamado, Ticket
from schemas import TicketCreate, TicketOut


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    client = await init_db()
    yield
    client.close()


app = FastAPI(title="HelpDesk API — Videoaula 6", lifespan=lifespan)


@app.post(
    "/tickets",
    response_model=TicketOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Chamados"],
)
async def criar_ticket(dados: TicketCreate) -> TicketOut:
    ticket = await Ticket(**dados.model_dump()).insert()
    return TicketOut.model_validate(ticket)


# >>> DEMONSTRAÇÃO 1: filtros combinados, montados conforme os parâmetros recebidos
@app.get("/tickets", response_model=list[TicketOut], tags=["Filtros"])
async def listar_com_filtros(
    status_: Annotated[StatusChamado | None, Query(alias="status")] = None,
    prioridade: Annotated[Prioridade | None, Query()] = None,
    tag: Annotated[str | None, Query(description="Contém esta tag")] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
) -> list[TicketOut]:
    filtros: list[object] = []
    if status_:
        filtros.append(Ticket.status == status_)
    if prioridade:
        filtros.append(Ticket.prioridade == prioridade)
    if tag:
        filtros.append(In(Ticket.tags, [tag.lower()]))  # tag dentro da lista

    tickets = (
        await Ticket.find(*filtros)  # type: ignore[arg-type]
        .sort("-criado_em")
        .skip(skip)
        .limit(limit)
        .to_list()
    )
    return [TicketOut.model_validate(t) for t in tickets]


# >>> DEMONSTRAÇÃO 2: busca textual (OU) e operadores
@app.get("/tickets/busca", response_model=list[TicketOut], tags=["Filtros"])
async def buscar(termo: Annotated[str, Query(min_length=2)]) -> list[TicketOut]:
    tickets = await Ticket.find(
        Or(
            RegEx(Ticket.titulo, termo, options="i"),  # "i" = ignora maiúsculas
            RegEx(Ticket.descricao, termo, options="i"),
        )
    ).to_list()
    return [TicketOut.model_validate(t) for t in tickets]


# >>> DEMONSTRAÇÃO 3: operadores de comparação (chamados antigos ainda abertos)
@app.get("/tickets/atrasados", response_model=list[TicketOut], tags=["Filtros"])
async def atrasados(dias: Annotated[int, Query(ge=1)] = 3) -> list[TicketOut]:
    limite = datetime.now(UTC) - timedelta(days=dias)
    tickets = await Ticket.find(
        Ticket.status == StatusChamado.ABERTO,
        Ticket.criado_em < limite,
    ).to_list()
    return [TicketOut.model_validate(t) for t in tickets]


# >>> DEMONSTRAÇÃO 4: AGREGAÇÃO — pipeline de etapas ($group, $sort)
@app.get("/relatorios/por-status", tags=["Relatórios"])
async def total_por_status() -> list[dict[str, object]]:
    pipeline = [
        {"$group": {"_id": "$status", "total": {"$sum": 1}}},
        {"$sort": {"total": -1}},
    ]
    resultado = await Ticket.aggregate(pipeline).to_list()
    return [{"status": r["_id"], "total": r["total"]} for r in resultado]


@app.get("/relatorios/por-prioridade-e-status", tags=["Relatórios"])
async def total_por_prioridade_e_status() -> list[dict[str, object]]:
    pipeline = [
        {"$match": {"status": {"$ne": "cancelado"}}},  # ignora cancelados
        {
            "$group": {
                "_id": {"prioridade": "$prioridade", "status": "$status"},
                "total": {"$sum": 1},
            }
        },
        {"$sort": {"_id.prioridade": 1, "_id.status": 1}},
    ]
    resultado = await Ticket.aggregate(pipeline).to_list()
    return [{**r["_id"], "total": r["total"]} for r in resultado]
