"""Contratos (Schemas) do HelpDesk: entrada e saída da API."""

from datetime import UTC, datetime
from typing import Self

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

from app.schemas.enums import Prioridade, StatusChamado

DOMINIOS_BLOQUEADOS = {"mailinator.com", "tempmail.com", "10minutemail.com"}


class TicketCreate(BaseModel):
    """Dados necessários para abrir um chamado (a 'catraca' de entrada)."""

    titulo: str = Field(min_length=5, max_length=100, examples=["Sem acesso à VPN"])
    descricao: str = Field(
        min_length=10,
        max_length=2000,
        examples=["Desde ontem não consigo conectar na VPN da empresa."],
    )
    email_solicitante: EmailStr
    prioridade: Prioridade = Prioridade.MEDIA
    tags: list[str] = Field(default_factory=list, max_length=5)

    @field_validator("email_solicitante")
    @classmethod
    def rejeitar_email_descartavel(cls, valor: str) -> str:
        valor = valor.lower()
        dominio = valor.split("@")[-1]
        if dominio in DOMINIOS_BLOQUEADOS:
            raise ValueError(f"o domínio '{dominio}' não é aceito pelo HelpDesk")
        return valor

    @field_validator("titulo", mode="before")
    @classmethod
    def limpar_titulo(cls, valor: object) -> object:
        if isinstance(valor, str):
            return " ".join(valor.split())
        return valor

    @field_validator("tags")
    @classmethod
    def normalizar_tags(cls, valor: list[str]) -> list[str]:
        return sorted({tag.strip().lower() for tag in valor if tag.strip()})

    @model_validator(mode="after")
    def prioridade_alta_exige_detalhes(self) -> Self:
        if self.prioridade == Prioridade.ALTA and len(self.descricao) < 30:
            raise ValueError(
                "chamados de prioridade ALTA exigem descrição com ao menos "
                "30 caracteres"
            )
        return self


class TicketStatusUpdate(BaseModel):
    """Corpo da requisição para mudar o status de um chamado."""

    status: StatusChamado


class TicketOut(BaseModel):
    """Chamado como é devolvido pela API."""

    id: int
    titulo: str
    descricao: str
    email_solicitante: EmailStr
    prioridade: Prioridade
    status: StatusChamado = StatusChamado.ABERTO
    tags: list[str] = Field(default_factory=list)
    criado_em: datetime = Field(default_factory=lambda: datetime.now(UTC))
