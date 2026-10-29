"""VIDEOAULA 10 — Modelos: chamado e atendente."""

from datetime import UTC, datetime
from enum import StrEnum

from beanie import Document, Indexed
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
        name = "tickets"


class Agente(Document):
    nome: str
    email: Indexed(EmailStr, unique=True)  # type: ignore[valid-type]
    senha_hash: str
    ativo: bool = True
    criado_em: datetime = Field(default_factory=agora)

    class Settings:
        name = "agentes"
