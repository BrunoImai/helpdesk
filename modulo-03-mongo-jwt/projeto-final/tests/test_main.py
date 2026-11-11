"""Testes básicos do HelpDesk (Aula 5): caminho feliz, validação e rotas protegidas.

Execute (na pasta projeto-final):  pytest -v
Nenhum teste aqui precisa de MongoDB.
"""

import pytest
from fastapi.testclient import TestClient

ID_QUALQUER = "64b7f0c2a1b2c3d4e5f60718"

CHAMADO_VALIDO = {
    "titulo": "Sem acesso à VPN",
    "descricao": "Desde ontem não consigo conectar na VPN da empresa.",
    "email_solicitante": "cliente@empresa.com",
}


# ---------------------------------------------------------------------------
# Caminho feliz
# ---------------------------------------------------------------------------
def test_api_esta_no_ar(client: TestClient) -> None:
    resposta = client.get("/")

    assert resposta.status_code == 200
    assert resposta.json()["status"] == "ok"


# ---------------------------------------------------------------------------
# Caminho de erro 1: dados inválidos -> 422 (o Pydantic barra antes do banco)
# ---------------------------------------------------------------------------
def test_chamado_com_email_invalido_devolve_422(client: TestClient) -> None:
    dados = {**CHAMADO_VALIDO, "email_solicitante": "isto-nao-e-um-email"}

    resposta = client.post("/tickets", json=dados)

    assert resposta.status_code == 422


def test_chamado_sem_titulo_devolve_422(client: TestClient) -> None:
    dados = {k: v for k, v in CHAMADO_VALIDO.items() if k != "titulo"}

    resposta = client.post("/tickets", json=dados)

    assert resposta.status_code == 422


def test_login_sem_enviar_campos_devolve_422(client: TestClient) -> None:
    resposta = client.post("/auth/login", data={})

    assert resposta.status_code == 422


# ---------------------------------------------------------------------------
# Caminho de erro 2: rota protegida sem token -> 401
# ---------------------------------------------------------------------------
ROTAS_DO_SUPORTE = [
    ("GET", "/tickets"),
    ("GET", f"/tickets/{ID_QUALQUER}"),
    ("DELETE", f"/tickets/{ID_QUALQUER}"),
    ("GET", "/auth/eu"),
]


@pytest.mark.parametrize(("metodo", "url"), ROTAS_DO_SUPORTE)
def test_rota_do_suporte_sem_token_devolve_401(
    client: TestClient, metodo: str, url: str
) -> None:
    resposta = client.request(metodo, url)

    assert resposta.status_code == 401
    assert resposta.headers["www-authenticate"] == "Bearer"


def test_token_invalido_devolve_401(client: TestClient) -> None:
    cabecalho = {"Authorization": "Bearer isto.nao.e-um-token"}

    resposta = client.get("/tickets", headers=cabecalho)

    assert resposta.status_code == 401
