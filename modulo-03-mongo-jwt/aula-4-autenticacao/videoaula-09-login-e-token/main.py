"""
VIDEOAULA 9 — Gerando e entregando o Token JWT no fluxo de login do atendente.

Execute:  uvicorn main:app --reload
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated

from database import init_db
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models import Agente
from schemas import Token
from security import criar_token_acesso, verificar_senha


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    client = await init_db()
    yield
    client.close()


app = FastAPI(title="HelpDesk API — Videoaula 9", lifespan=lifespan)


# >>> DEMONSTRAÇÃO: o endpoint de login
#     OAuth2PasswordRequestForm lê um formulário com os campos `username` e `password`
#     (assim o botão "Authorize" do Swagger também funciona).
@app.post("/auth/login", response_model=Token, tags=["Autenticação"])
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    agente = await Agente.find_one(Agente.email == form.username.lower())

    # Mesma mensagem para "e-mail não existe" e "senha errada": não revela quem está cadastrado
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
