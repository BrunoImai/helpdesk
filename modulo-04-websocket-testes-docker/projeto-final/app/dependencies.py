"""Dependências compartilhadas entre os routers (injeção com `Depends`)."""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer

from app.core.security import decodificar_token
from app.models.agente import Agente
from app.services import agente_service
from app.services.ticket_service import TicketService


# ---------------------------------------------------------------------------
# Serviço de chamados
# ---------------------------------------------------------------------------
@lru_cache
def get_ticket_service() -> TicketService:
    return TicketService()


TicketServiceDep = Annotated[TicketService, Depends(get_ticket_service)]


# ---------------------------------------------------------------------------
# Paginação
# ---------------------------------------------------------------------------
class Paginacao:
    def __init__(
        self,
        skip: Annotated[int, Query(ge=0, description="Quantos itens pular")] = 0,
        limit: Annotated[int, Query(ge=1, le=100, description="Máximo de itens")] = 10,
    ) -> None:
        self.skip = skip
        self.limit = limit


PaginacaoDep = Annotated[Paginacao, Depends()]

# ---------------------------------------------------------------------------
# Autenticação: o "crachá" (token JWT) exigido nas rotas do suporte
# ---------------------------------------------------------------------------
# `tokenUrl` aponta para a rota de login; o Swagger usa isso no botão "Authorize".
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_agente_atual(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> Agente:
    """Valida o token e devolve o atendente dono dele (ou responde 401)."""
    erro_credenciais = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = decodificar_token(token)
    if email is None:
        raise erro_credenciais

    agente = await agente_service.buscar_por_email(email)
    if agente is None or not agente.ativo:
        raise erro_credenciais
    return agente


AgenteAtual = Annotated[Agente, Depends(get_agente_atual)]
