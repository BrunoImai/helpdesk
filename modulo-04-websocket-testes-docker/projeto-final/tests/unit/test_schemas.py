"""TESTES DE UNIDADE: as "catracas" (schemas Pydantic) do HelpDesk."""

from typing import Any

import pytest
from pydantic import ValidationError

from app.schemas.ticket import TicketCreate

BASE: dict[str, Any] = {
    "titulo": "Sem acesso à VPN",
    "descricao": "Desde ontem não consigo conectar na VPN da empresa.",
    "email_solicitante": "ana@empresa.com",
}


def test_chamado_valido_e_aceito() -> None:
    ticket = TicketCreate(**BASE)
    assert ticket.prioridade == "media"  # valor padrão
    assert ticket.tags == []


def test_email_e_normalizado_para_minusculas() -> None:
    ticket = TicketCreate(**{**BASE, "email_solicitante": "Ana@Empresa.COM"})
    assert ticket.email_solicitante == "ana@empresa.com"


@pytest.mark.parametrize(
    "email",
    ["sem-arroba.com", "ana@", "@empresa.com", "ana@@empresa.com", ""],
)
def test_email_malformado_e_rejeitado(email: str) -> None:
    with pytest.raises(ValidationError) as erro:
        TicketCreate(**{**BASE, "email_solicitante": email})
    assert erro.value.errors()[0]["loc"] == ("email_solicitante",)


def test_email_descartavel_e_rejeitado() -> None:
    with pytest.raises(ValidationError, match="não é aceito"):
        TicketCreate(**{**BASE, "email_solicitante": "joao@mailinator.com"})


def test_titulo_com_espacos_extras_e_limpo() -> None:
    ticket = TicketCreate(**{**BASE, "titulo": "  Sem   acesso   à VPN  "})
    assert ticket.titulo == "Sem acesso à VPN"


@pytest.mark.parametrize("campo", ["titulo", "descricao", "email_solicitante"])
def test_campo_obrigatorio_ausente(campo: str) -> None:
    dados = {k: v for k, v in BASE.items() if k != campo}
    with pytest.raises(ValidationError):
        TicketCreate(**dados)


def test_prioridade_invalida_e_rejeitada() -> None:
    with pytest.raises(ValidationError):
        TicketCreate(**{**BASE, "prioridade": "urgentissima"})


def test_prioridade_alta_exige_descricao_detalhada() -> None:
    with pytest.raises(ValidationError, match="ALTA"):
        TicketCreate(**{**BASE, "prioridade": "alta", "descricao": "Muito urgente!!!"})


def test_tags_sao_normalizadas() -> None:
    ticket = TicketCreate(**{**BASE, "tags": [" VPN ", "rede", "vpn", ""]})
    assert ticket.tags == ["rede", "vpn"]
