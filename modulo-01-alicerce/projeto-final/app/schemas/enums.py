"""Valores fixos do domínio do HelpDesk."""

from enum import StrEnum


class StatusChamado(StrEnum):
    ABERTO = "aberto"
    EM_ANDAMENTO = "em_andamento"
    RESOLVIDO = "resolvido"
    CANCELADO = "cancelado"


class Prioridade(StrEnum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
