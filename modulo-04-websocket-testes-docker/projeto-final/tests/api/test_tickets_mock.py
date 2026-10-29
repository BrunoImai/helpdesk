"""ISOLAMENTO COM MOCKS (Videoaula 6): testando as rotas SEM banco de dados.

Técnica: `app.dependency_overrides` troca, só durante o teste, o serviço real por um
serviço FALSO em memória. Assim o banco de produção nunca é tocado ("sujo") e o teste
roda em milissegundos.
"""

from collections.abc import Iterator
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock

import pytest
from beanie import PydanticObjectId
from fastapi.testclient import TestClient

from app.dependencies import get_agente_atual, get_ticket_service
from app.main import app
from app.schemas.ticket import TicketCreate, TicketOut
from app.services.ticket_service import TicketNotFoundError


class ServicoFalso:
    """Imita o TicketService guardando tudo em um dicionário."""

    def __init__(self) -> None:
        self.tickets: dict[PydanticObjectId, TicketOut] = {}

    async def criar(self, dados: TicketCreate) -> TicketOut:
        ticket = TicketOut(
            id=PydanticObjectId(),
            status="aberto",  # type: ignore[arg-type]
            criado_em="2026-01-01T10:00:00Z",  # type: ignore[arg-type]
            **dados.model_dump(),
        )
        self.tickets[ticket.id] = ticket
        return ticket

    async def listar(self, **_: Any) -> list[TicketOut]:
        return list(self.tickets.values())

    async def buscar(self, ticket_id: PydanticObjectId) -> TicketOut:
        if ticket_id not in self.tickets:
            raise TicketNotFoundError(ticket_id)
        return self.tickets[ticket_id]


@pytest.fixture
def servico_falso() -> Iterator[ServicoFalso]:
    servico = ServicoFalso()
    app.dependency_overrides[get_ticket_service] = lambda: servico
    # "Pula" a autenticação: finge que há um atendente logado
    app.dependency_overrides[get_agente_atual] = lambda: SimpleNamespace(
        email="teste@helpdesk.com", ativo=True
    )
    yield servico
    app.dependency_overrides.clear()  # SEMPRE limpar, senão vaza para outros testes


@pytest.fixture
def client_mock(servico_falso: ServicoFalso) -> TestClient:
    # Sem `with`: o lifespan não roda, então nenhuma conexão com o banco é criada
    return TestClient(app)


DADOS = {
    "titulo": "Sem acesso à VPN",
    "descricao": "Desde ontem não consigo conectar na VPN da empresa.",
    "email_solicitante": "ana@empresa.com",
}


def test_criar_chamado_nao_usa_banco(
    client_mock: TestClient,
    servico_falso: ServicoFalso,
    sem_envio_de_email: AsyncMock,
) -> None:
    # `sem_envio_de_email` (conftest.py) é um mock do envio de e-mail: nada é enviado
    # de verdade e o teste não espera os 2 s da simulação.
    resposta = client_mock.post("/tickets", json=DADOS)

    assert resposta.status_code == 201
    assert len(servico_falso.tickets) == 1
    sem_envio_de_email.assert_awaited_once()  # a tarefa de fundo foi executada
    assert sem_envio_de_email.await_args.args[0] == "ana@empresa.com"


def test_listar_devolve_o_que_o_servico_falso_tem(
    client_mock: TestClient,
) -> None:
    client_mock.post("/tickets", json=DADOS)
    client_mock.post("/tickets", json={**DADOS, "titulo": "Impressora travada"})

    resposta = client_mock.get("/tickets")

    assert resposta.status_code == 200
    assert [t["titulo"] for t in resposta.json()] == [
        "Sem acesso à VPN",
        "Impressora travada",
    ]


def test_chamado_inexistente_devolve_404_humanizado(client_mock: TestClient) -> None:
    resposta = client_mock.get("/tickets/64b7f0c2a1b2c3d4e5f60718")

    assert resposta.status_code == 404
    assert "não encontrado" in resposta.json()["detail"]


def test_id_malformado_devolve_422(client_mock: TestClient) -> None:
    resposta = client_mock.get("/tickets/isto-nao-e-um-objectid")
    assert resposta.status_code == 422


def test_dados_invalidos_nem_chegam_ao_servico(
    client_mock: TestClient, servico_falso: ServicoFalso
) -> None:
    resposta = client_mock.post("/tickets", json={**DADOS, "email_solicitante": "x"})

    assert resposta.status_code == 422
    assert servico_falso.tickets == {}  # a catraca barrou antes
