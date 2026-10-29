"""
VIDEOAULA 9 — Primeiro Schema Pydantic do HelpDesk: TicketCreate.
"""

from enum import StrEnum

from pydantic import BaseModel, EmailStr, Field


class Prioridade(StrEnum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"


class TicketCreate(BaseModel):
    """Contrato de entrada para abrir um chamado."""

    titulo: str = Field(min_length=5, max_length=100, examples=["Sem acesso à VPN"])
    descricao: str = Field(min_length=10, max_length=2000)
    email_solicitante: EmailStr
    prioridade: Prioridade = Prioridade.MEDIA
    tags: list[str] = Field(default_factory=list, max_length=5)
