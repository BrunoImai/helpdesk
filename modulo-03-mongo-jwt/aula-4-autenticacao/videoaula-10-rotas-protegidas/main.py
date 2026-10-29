"""
VIDEOAULA 10 — Exigindo o "crachá" (Depends) em rotas exclusivas para o suporte.

Execute:  uvicorn main:app --reload
No Swagger: botão "Authorize" -> e-mail e senha do atendente.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Annotated

from beanie import PydanticObjectId
from database import init_db
from dependencies import AgenteAtual, get_agente_atual
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from models import Agente, Ticket
from schemas import (
    AgenteOut,
    TicketCreate,
    TicketOut,
    TicketStatusUpdate,
    Token,
)
from security import criar_token_acesso, verificar_senha


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    client = await init_db()
    yield
    client.close()


app = FastAPI(title="HelpDesk API — Videoaula 10", lifespan=lifespan)


# ---------------------------------------------------------------------------
# Login (público) — visto na Videoaula 9
# ---------------------------------------------------------------------------
@app.post("/auth/login", response_model=Token, tags=["Autenticação"])
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    agente = await Agente.find_one(Agente.email == form.username.lower())
    if (
        agente is None
        or not agente.ativo
        or not verificar_senha(form.password, agente.senha_hash)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=criar_token_acesso(agente.email))


# ---------------------------------------------------------------------------
# >>> DEMONSTRAÇÃO 1: rota protegida que USA o atendente logado
# ---------------------------------------------------------------------------
@app.get("/auth/eu", response_model=AgenteOut, tags=["Autenticação"])
async def quem_sou_eu(agente: AgenteAtual) -> AgenteOut:
    return AgenteOut.model_validate(agente)


# ---------------------------------------------------------------------------
# Rota PÚBLICA: o cliente abre o chamado sem login
# ---------------------------------------------------------------------------
@app.post(
    "/tickets",
    response_model=TicketOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Chamados"],
)
async def criar_ticket(dados: TicketCreate) -> TicketOut:
    ticket = await Ticket(**dados.model_dump()).insert()
    return TicketOut.model_validate(ticket)


# ---------------------------------------------------------------------------
# >>> DEMONSTRAÇÃO 2: rota protegida que NÃO precisa do atendente na função
#     `dependencies=[Depends(...)]` executa a verificação, mas ignora o retorno.
# ---------------------------------------------------------------------------
@app.get(
    "/tickets",
    response_model=list[TicketOut],
    dependencies=[Depends(get_agente_atual)],
    tags=["Chamados"],
)
async def listar_tickets() -> list[TicketOut]:
    tickets = await Ticket.find_all().sort("-criado_em").to_list()
    return [TicketOut.model_validate(t) for t in tickets]


# ---------------------------------------------------------------------------
# >>> DEMONSTRAÇÃO 3: rota de edição trancada (o desafio do módulo)
# ---------------------------------------------------------------------------
@app.patch(
    "/tickets/{ticket_id}/status",
    response_model=TicketOut,
    tags=["Chamados"],
)
async def alterar_status(
    ticket_id: PydanticObjectId,
    dados: TicketStatusUpdate,
    agente: AgenteAtual,  # <- sem token válido, nem entra na função (401)
) -> TicketOut:
    ticket = await Ticket.get(ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    await ticket.set({"status": dados.status, "atualizado_em": datetime.now(UTC)})
    print(f"Status do chamado {ticket_id} alterado por {agente.email}")  # auditoria
    return TicketOut.model_validate(ticket)


@app.delete(
    "/tickets/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_agente_atual)],
    tags=["Chamados"],
)
async def apagar_ticket(ticket_id: PydanticObjectId) -> Response:
    ticket = await Ticket.get(ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    await ticket.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
