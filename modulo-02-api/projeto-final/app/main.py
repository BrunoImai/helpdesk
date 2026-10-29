"""Ponto de entrada da API do HelpDesk.

Execute (na pasta projeto-final):
    uvicorn app.main:app --reload
Swagger: http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.routers import tickets
from app.services.ticket_service import TicketNotFoundError

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="2.0.0",
    description=(
        "API do **HelpDesk** da trilha *Dominando Python para Web*.\n\n"
        "Abra, consulte, atualize e encerre chamados de suporte."
    ),
    openapi_tags=[{"name": "Chamados", "description": "Operações da fila de chamados"}],
)

app.include_router(tickets.router)


@app.exception_handler(TicketNotFoundError)
async def ticket_nao_encontrado(_: Request, erro: TicketNotFoundError) -> JSONResponse:
    """Traduz o erro de negócio em uma resposta HTTP 404 amigável."""
    return JSONResponse(
        status_code=404,
        content={
            "detail": (
                f"Chamado #{erro.ticket_id} não encontrado. "
                "Confira o número e tente novamente."
            )
        },
    )


@app.get("/", tags=["Saúde"], summary="Verificar se a API está no ar")
async def health() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name}
