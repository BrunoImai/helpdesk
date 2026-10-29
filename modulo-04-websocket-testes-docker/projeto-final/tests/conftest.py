"""Fixtures compartilhadas por todos os testes.

REGRA DE OURO: os testes NUNCA tocam no banco real. As variáveis abaixo são definidas
ANTES de importar a aplicação, e o Motor é trocado por um MongoDB falso em memória.
"""

import os

# Variáveis de ambiente têm prioridade sobre o arquivo .env
os.environ["SECRET_KEY"] = "chave-secreta-somente-para-testes-0123456789abcdef"
os.environ["MONGO_URI"] = "mongodb://banco-que-nunca-sera-usado:27017"
os.environ["MONGO_DB_NAME"] = "helpdesk_testes"

from collections.abc import Iterator  # noqa: E402
from typing import Any  # noqa: E402
from unittest.mock import AsyncMock  # noqa: E402

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from mongomock_motor import AsyncMongoMockClient  # noqa: E402

import app.core.database as database  # noqa: E402
from app.main import app  # noqa: E402
from app.services.agente_service import criar_agente  # noqa: E402

EMAIL_AGENTE = "ana@helpdesk.com"
SENHA_AGENTE = "senha-forte-123"


@pytest.fixture(autouse=True)
def sem_envio_de_email(monkeypatch: pytest.MonkeyPatch) -> AsyncMock:
    """Nenhum teste envia e-mail de verdade (nem espera os 2 s da simulação)."""
    falso = AsyncMock()
    monkeypatch.setattr("app.routers.tickets.enviar_email_confirmacao", falso)
    return falso


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    """Cliente HTTP ligado a um MongoDB falso, novo e vazio a cada teste."""
    monkeypatch.setattr(database, "AsyncIOMotorClient", AsyncMongoMockClient)
    with TestClient(app) as test_client:  # `with` executa o lifespan (init_db)
        yield test_client


@pytest.fixture
def agente(client: TestClient) -> dict[str, str]:
    """Cria um atendente no banco falso."""
    client.portal.call(criar_agente, "Ana Souza", EMAIL_AGENTE, SENHA_AGENTE)  # type: ignore[union-attr]
    return {"email": EMAIL_AGENTE, "senha": SENHA_AGENTE}


@pytest.fixture
def token(client: TestClient, agente: dict[str, str]) -> str:
    """Token JWT válido do atendente."""
    resposta = client.post(
        "/auth/login",
        data={"username": agente["email"], "password": agente["senha"]},
    )
    assert resposta.status_code == 200
    return str(resposta.json()["access_token"])


@pytest.fixture
def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def ticket_payload() -> dict[str, Any]:
    return {
        "titulo": "Sem acesso à VPN",
        "descricao": "Desde ontem não consigo conectar na VPN da empresa.",
        "email_solicitante": "cliente@empresa.com",
        "prioridade": "media",
        "tags": ["vpn"],
    }


@pytest.fixture
def ticket_criado(client: TestClient, ticket_payload: dict[str, Any]) -> dict[str, Any]:
    """Um chamado já gravado no banco falso (criado pela rota pública)."""
    resposta = client.post("/tickets", json=ticket_payload)
    assert resposta.status_code == 201
    return dict(resposta.json())
