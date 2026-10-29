"""Modelo (documento) de atendente do suporte."""

from datetime import UTC, datetime

from beanie import Document, Indexed
from pydantic import EmailStr, Field


class Agente(Document):
    nome: str
    email: Indexed(EmailStr, unique=True)  # type: ignore[valid-type]
    senha_hash: str  # NUNCA guardamos a senha em texto puro
    ativo: bool = True
    criado_em: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Settings:
        name = "agentes"
