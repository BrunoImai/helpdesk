"""Teste de fumaça manual: percorre o fluxo completo SEM precisar de um MongoDB.

Usa o `mongomock-motor` (banco falso em memória) no lugar do Motor real.
Execute (na pasta projeto-final):
    python smoke_test.py
Os testes automatizados de verdade estão em tests/ (Aula 5).
"""

import os

# Configuração mínima só para este teste (não depende do seu .env)
os.environ.setdefault("SECRET_KEY", "chave-apenas-para-smoke-test-0123456789abcdef")

from mongomock_motor import AsyncMongoMockClient  # noqa: E402

import app.core.database as database  # noqa: E402

database.AsyncIOMotorClient = AsyncMongoMockClient  # type: ignore[misc]

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402
from app.services.agente_service import criar_agente  # noqa: E402

NOVO = {
    "titulo": "Sem acesso à VPN",
    "descricao": "Desde ontem não consigo conectar na VPN da empresa.",
    "email_solicitante": "ana@empresa.com",
}


def mostrar(passo: str, resposta) -> None:  # noqa: ANN001
    print(f"{passo:<38} -> {resposta.status_code} {resposta.text[:70]}")


with TestClient(app) as client:  # `with` executa o lifespan (init_db)
    client.portal.call(criar_agente, "Ana Souza", "ana@helpdesk.com", "senha-forte-123")

    criado = client.post("/tickets", json=NOVO)
    mostrar("POST /tickets (público)", criado)
    ticket_id = criado.json()["id"]

    mostrar("GET /tickets (sem token)", client.get("/tickets"))
    mostrar(
        "POST /auth/login (senha errada)",
        client.post(
            "/auth/login", data={"username": "ana@helpdesk.com", "password": "x"}
        ),
    )

    login = client.post(
        "/auth/login",
        data={"username": "ana@helpdesk.com", "password": "senha-forte-123"},
    )
    mostrar("POST /auth/login", login)
    cabecalho = {"Authorization": f"Bearer {login.json()['access_token']}"}

    mostrar("GET /auth/eu", client.get("/auth/eu", headers=cabecalho))
    mostrar("GET /tickets", client.get("/tickets", headers=cabecalho))
    mostrar(
        "PATCH status -> resolvido",
        client.patch(
            f"/tickets/{ticket_id}/status",
            json={"status": "resolvido"},
            headers=cabecalho,
        ),
    )
    mostrar(
        "GET /tickets/resolvidos", client.get("/tickets/resolvidos", headers=cabecalho)
    )
    mostrar("GET /tickets/resumo", client.get("/tickets/resumo", headers=cabecalho))
    mostrar(
        "GET /tickets/<id inexistente>",
        client.get("/tickets/64b7f0c2a1b2c3d4e5f60718", headers=cabecalho),
    )
    mostrar(
        "DELETE /tickets/<id>",
        client.delete(f"/tickets/{ticket_id}", headers=cabecalho),
    )
    mostrar("DELETE sem token", client.delete(f"/tickets/{ticket_id}"))
