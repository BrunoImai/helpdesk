"""
VIDEOAULA 10 — TicketCreate com validadores customizados.
"""

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

# Domínios de e-mail descartável que o HelpDesk não aceita
DOMINIOS_BLOQUEADOS = {"mailinator.com", "tempmail.com", "10minutemail.com"}


class Prioridade(StrEnum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"


class TicketCreate(BaseModel):
    titulo: str = Field(min_length=5, max_length=100)
    descricao: str = Field(min_length=10, max_length=2000)
    email_solicitante: EmailStr
    prioridade: Prioridade = Prioridade.MEDIA
    tags: list[str] = Field(default_factory=list, max_length=5)

    # >>> DEMONSTRAÇÃO 1: validar e normalizar o e-mail
    @field_validator("email_solicitante")
    @classmethod
    def rejeitar_email_descartavel(cls, valor: str) -> str:
        valor = valor.lower()
        dominio = valor.split("@")[-1]
        if dominio in DOMINIOS_BLOQUEADOS:
            raise ValueError(f"o domínio '{dominio}' não é aceito pelo HelpDesk")
        return valor

    # >>> DEMONSTRAÇÃO 2: limpar o texto ANTES da validação de tamanho
    @field_validator("titulo", mode="before")
    @classmethod
    def limpar_titulo(cls, valor: object) -> object:
        if isinstance(valor, str):
            return " ".join(valor.split())  # remove espaços extras
        return valor

    # >>> DEMONSTRAÇÃO 3: normalizar a lista de tags
    @field_validator("tags")
    @classmethod
    def normalizar_tags(cls, valor: list[str]) -> list[str]:
        limpas = {tag.strip().lower() for tag in valor if tag.strip()}
        return sorted(limpas)  # sem repetição, minúsculas e em ordem

    # >>> DEMONSTRAÇÃO 4: regra que envolve mais de um campo
    @model_validator(mode="after")
    def prioridade_alta_exige_detalhes(self) -> Self:
        if self.prioridade == Prioridade.ALTA and len(self.descricao) < 30:
            raise ValueError(
                "chamados de prioridade ALTA exigem descrição com ao menos 30 caracteres"
            )
        return self
