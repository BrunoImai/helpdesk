"""Ponto de entrada da API do HelpDesk (Módulo 3: MongoDB + JWT).

Execute (na pasta projeto-final):
    uvicorn app.main:app --reload
Swagger: http://127.0.0.1:8000/docs  (use o botão "Authorize" para informar o login)
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.database import init_db
from app.routers import auth, tickets
from app.services.ticket_service import TicketNotFoundError

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Roda ao ligar (conecta no banco) e ao desligar (fecha a conexão)."""
    client = await init_db()
    yield
    if client is not None:
        client.close()


app = FastAPI(
    title=settings.app_name,
    version="3.0.0",
    description=(
        "API do **HelpDesk** da trilha *Dominando Python para Web*.\n\n"
        "Chamados persistidos no **MongoDB** e rotas do suporte protegidas por **JWT**."
    ),
    openapi_tags=[
        {"name": "Chamados", "description": "Operações da fila de chamados"},
        {"name": "Autenticação", "description": "Login dos atendentes"},
    ],
    lifespan=lifespan,
)

app.include_router(auth.router)
app.include_router(tickets.router)


@app.exception_handler(TicketNotFoundError)
async def ticket_nao_encontrado(_: Request, erro: TicketNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "detail": (
                f"Chamado {erro.ticket_id} não encontrado. "
                "Confira o identificador e tente novamente."
            )
        },
    )


@app.get("/", tags=["Saúde"], summary="Verificar se a API está no ar")
async def health() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name}
