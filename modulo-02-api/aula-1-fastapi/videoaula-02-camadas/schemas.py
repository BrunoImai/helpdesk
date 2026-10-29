"""VIDEOAULA 2 — Contratos Pydantic (versão enxuta)."""

from pydantic import BaseModel, EmailStr, Field


class TicketCreate(BaseModel):
    titulo: str = Field(min_length=5, max_length=100)
    descricao: str = Field(min_length=10)
    email_solicitante: EmailStr


class TicketOut(TicketCreate):
    id: int
    status: str = "aberto"
