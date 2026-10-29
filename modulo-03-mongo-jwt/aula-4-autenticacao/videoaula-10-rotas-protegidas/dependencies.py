"""VIDEOAULA 10 — A dependência que confere o "crachá" (token JWT)."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from models import Agente
from security import decodificar_token

# `tokenUrl` diz ao Swagger onde fazer o login (habilita o botão "Authorize").
# Esta classe também extrai o token do cabeçalho `Authorization: Bearer <token>`.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# >>> DEMONSTRAÇÃO: a dependência do crachá
async def get_agente_atual(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> Agente:
    erro_401 = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    email = decodificar_token(token)  # 1. assinatura e validade
    if email is None:
        raise erro_401

    agente = await Agente.find_one(
        Agente.email == email
    )  # 2. o atendente ainda existe?
    if agente is None or not agente.ativo:
        raise erro_401
    return agente


# Atalho para usar nas rotas: `agente: AgenteAtual`
AgenteAtual = Annotated[Agente, Depends(get_agente_atual)]
