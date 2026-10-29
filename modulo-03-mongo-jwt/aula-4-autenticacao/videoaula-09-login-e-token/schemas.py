"""VIDEOAULA 9 — Contratos de autenticação."""

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
