"""Modelo (documento) de chamado no MongoDB."""

from datetime import UTC, datetime

from beanie import Document
from pydantic import BaseModel, EmailStr, Field

from app.schemas.enums import Prioridade, StatusChamado


def agora() -> datetime:
    return datetime.now(UTC)


class Mensagem(BaseModel):
    """Mensagem do histórico do chamado (documento EMBUTIDO dentro do chamado)."""

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
        name = "tickets"  # nome da coleção
        indexes = ["status", "prioridade", [("criado_em", -1)]]
