"""ERROS E ROTAS AUTENTICADAS (Videoaula 7): login, 401 e acesso com token."""

from datetime import timedelta
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.core.security import criar_token_acesso
from tests.conftest import EMAIL_AGENTE, SENHA_AGENTE


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------
def test_login_com_dados_corretos_devolve_token(
    client: TestClient, agente: dict[str, str]
) -> None:
    resposta = client.post(
        "/auth/login", data={"username": EMAIL_AGENTE, "password": SENHA_AGENTE}
    )
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["token_type"] == "bearer"
    assert corpo["access_token"].count(".") == 2  # header.payload.signature


def test_login_com_senha_errada_devolve_401(
    client: TestClient, agente: dict[str, str]
) -> None:
    resposta = client.post(
        "/auth/login", data={"username": EMAIL_AGENTE, "password": "senha-errada"}
    )
    assert resposta.status_code == 401
    assert resposta.json()["detail"] == "E-mail ou senha incorretos"


def test_login_com_email_inexistente_tem_a_mesma_resposta_da_senha_errada(
    client: TestClient, agente: dict[str, str]
) -> None:
    """Não revelar quais e-mails existem (evita enumeração de usuários)."""
    errada = client.post(
        "/auth/login", data={"username": EMAIL_AGENTE, "password": "x"}
    )
    inexistente = client.post(
        "/auth/login", data={"username": "fantasma@helpdesk.com", "password": "x"}
    )
    assert errada.status_code == inexistente.status_code == 401
    assert errada.json() == inexistente.json()


def test_login_sem_enviar_campos_devolve_422(client: TestClient) -> None:
    assert client.post("/auth/login", data={}).status_code == 422


# ---------------------------------------------------------------------------
# Rotas protegidas SEM token válido -> 401
# ---------------------------------------------------------------------------
ROTAS_DO_SUPORTE: list[tuple[str, str, dict[str, Any] | None]] = [
    ("GET", "/tickets", None),
    ("GET", "/tickets/resolvidos", None),
    ("GET", "/tickets/resumo", None),
    ("GET", "/tickets/64b7f0c2a1b2c3d4e5f60718", None),
    ("PATCH", "/tickets/64b7f0c2a1b2c3d4e5f60718/status", {"status": "resolvido"}),
    ("DELETE", "/tickets/64b7f0c2a1b2c3d4e5f60718", None),
    ("GET", "/auth/eu", None),
]


@pytest.mark.parametrize(("metodo", "url", "corpo"), ROTAS_DO_SUPORTE)
def test_rotas_do_suporte_sem_token_devolvem_401(
    client: TestClient, metodo: str, url: str, corpo: dict[str, Any] | None
) -> None:
    resposta = client.request(metodo, url, json=corpo)
    assert resposta.status_code == 401
    assert resposta.headers["www-authenticate"] == "Bearer"


def test_token_lixo_devolve_401(client: TestClient) -> None:
    resposta = client.get(
        "/tickets", headers={"Authorization": "Bearer lixo.lixo.lixo"}
    )
    assert resposta.status_code == 401


def test_token_expirado_devolve_401(client: TestClient, agente: dict[str, str]) -> None:
    expirado = criar_token_acesso(EMAIL_AGENTE, expira_em=timedelta(seconds=-5))
    resposta = client.get("/tickets", headers={"Authorization": f"Bearer {expirado}"})
    assert resposta.status_code == 401


def test_token_de_atendente_que_nao_existe_mais_devolve_401(client: TestClient) -> None:
    token = criar_token_acesso(
        "demitido@helpdesk.com"
    )  # assinatura válida, mas sem cadastro
    resposta = client.get("/tickets", headers={"Authorization": f"Bearer {token}"})
    assert resposta.status_code == 401


# ---------------------------------------------------------------------------
# Rotas protegidas COM token válido -> 200
# ---------------------------------------------------------------------------
def test_quem_sou_eu_com_token_valido(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    resposta = client.get("/auth/eu", headers=auth_headers)
    assert resposta.status_code == 200
    assert resposta.json()["email"] == EMAIL_AGENTE
    assert "senha" not in resposta.text  # nunca expõe senha nem hash


def test_abrir_chamado_nao_exige_login(
    client: TestClient, ticket_payload: dict[str, Any]
) -> None:
    assert client.post("/tickets", json=ticket_payload).status_code == 201
