"""VIDEOAULA 3 — Modelo (documento) do chamado com Beanie."""

from datetime import UTC, datetime
from enum import StrEnum

from beanie import Document
from pydantic import BaseModel, EmailStr, Field


def agora() -> datetime:
    return datetime.now(UTC)


class StatusChamado(StrEnum):
    ABERTO = "aberto"
    EM_ANDAMENTO = "em_andamento"
    RESOLVIDO = "resolvido"
    CANCELADO = "cancelado"


class Prioridade(StrEnum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"


class Mensagem(BaseModel):
    autor: str
    texto: str
    enviada_em: datetime = Field(default_factory=agora)


class Ticket(Document):
    titulo: str
    descricao: str
    email_solicitante: EmailStr
    prioridade: Prioridade = Prioridade.MEDIA
    status: StatusChamado = StatusChamado.ABERTO
    tags: list[str] = Field(default_factory=list)
    mensagens: list[Mensagem] = Field(default_factory=list)
    criado_em: datetime = Field(default_factory=agora)
    atualizado_em: datetime | None = None

    class Settings:
        name = "tickets"  # nome da coleção no MongoDB
