"""
VIDEOAULA 4 — Parâmetros de rota, de query e erros humanizados.

Execute:  uvicorn main:app --reload
"""

from enum import StrEnum
from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI(title="HelpDesk API — Videoaula 4")


class Status(StrEnum):
    ABERTO = "aberto"
    EM_ANDAMENTO = "em_andamento"
    RESOLVIDO = "resolvido"


class Prioridade(StrEnum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"


FILA = [
    {"id": 1, "titulo": "Sem internet", "status": "aberto", "prioridade": "alta"},
    {
        "id": 2,
        "titulo": "Impressora travada",
        "status": "em_andamento",
        "prioridade": "baixa",
    },
    {"id": 3, "titulo": "VPN não conecta", "status": "aberto", "prioridade": "media"},
    {"id": 4, "titulo": "Senha expirada", "status": "resolvido", "prioridade": "alta"},
]


# >>> DEMONSTRAÇÃO 1: parâmetros de QUERY (filtros opcionais + paginação)
@app.get("/tickets", tags=["Chamados"])
def listar(
    status: Annotated[Status | None, Query(description="Filtra pelo status")] = None,
    prioridade: Annotated[Prioridade | None, Query()] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
) -> list[dict[str, object]]:
    itens = FILA
    if status:
        itens = [t for t in itens if t["status"] == status.value]
    if prioridade:
        itens = [t for t in itens if t["prioridade"] == prioridade.value]
    return itens[skip : skip + limit]


# >>> DEMONSTRAÇÃO 2: rota fixa ANTES da rota com parâmetro
@app.get("/tickets/busca", tags=["Chamados"])
def buscar_por_termo(
    termo: Annotated[str, Query(min_length=2, max_length=50)],
) -> list[dict[str, object]]:
    return [t for t in FILA if termo.lower() in str(t["titulo"]).lower()]


# >>> DEMONSTRAÇÃO 3: parâmetro de ROTA validado + erro humanizado
@app.get("/tickets/{ticket_id}", tags=["Chamados"])
def obter(
    ticket_id: Annotated[int, Path(ge=1, description="Número do chamado")],
) -> dict[str, object]:
    for ticket in FILA:
        if ticket["id"] == ticket_id:
            return ticket
    raise HTTPException(
        status_code=404,
        detail=f"Não encontramos o chamado #{ticket_id}. Confira o número informado.",
    )


# >>> DEMONSTRAÇÃO 4: padronizando o erro de validação (422)
@app.exception_handler(RequestValidationError)
async def erro_de_validacao(_: Request, erro: RequestValidationError) -> JSONResponse:
    problemas = [
        {
            "campo": ".".join(str(parte) for parte in e["loc"][1:]),
            "problema": e["msg"],
        }
        for e in erro.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={"mensagem": "Algum dado enviado está incorreto", "erros": problemas},
    )
