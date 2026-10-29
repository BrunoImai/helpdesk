"""VIDEOAULA 3 — Contratos de entrada e saída (versão enxuta)."""

from datetime import datetime

from beanie import PydanticObjectId
from models import Prioridade, StatusChamado
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class TicketCreate(BaseModel):
    titulo: str = Field(min_length=5, max_length=100)
    descricao: str = Field(min_length=10, max_length=2000)
    email_solicitante: EmailStr
    prioridade: Prioridade = Prioridade.MEDIA
    tags: list[str] = Field(default_factory=list)


class TicketStatusUpdate(BaseModel):
    status: StatusChamado


class TicketOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: PydanticObjectId
    titulo: str
    descricao: str
    email_solicitante: EmailStr
    prioridade: Prioridade
    status: StatusChamado
    tags: list[str]
    criado_em: datetime
    atualizado_em: datetime | None = None
