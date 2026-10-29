"""Endpoints de autenticação dos atendentes."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import criar_token_acesso
from app.dependencies import AgenteAtual
from app.schemas.auth import AgenteOut, Token
from app.services import agente_service

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post(
    "/login",
    response_model=Token,
    summary="Entrar (gera o token JWT do atendente)",
)
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """O formulário OAuth2 usa os campos `username` (o e-mail) e `password`."""
    agente = await agente_service.autenticar(form.username, form.password)
    if agente is None:
        # Mesma mensagem para e-mail inexistente e senha errada (não vaza informação)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=criar_token_acesso(agente.email))


@router.get("/eu", response_model=AgenteOut, summary="Quem sou eu? (rota protegida)")
async def quem_sou_eu(agente: AgenteAtual) -> AgenteOut:
    return AgenteOut.model_validate(agente)
