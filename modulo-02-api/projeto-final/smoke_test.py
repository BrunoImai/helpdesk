"""Teste de fumaça manual (sem pytest): percorre o fluxo completo da API.

Execute (na pasta projeto-final):
    python smoke_test.py
Os testes automatizados de verdade entram no Módulo 3 (Aula 5).
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

novo = {
    "titulo": "Sem acesso à VPN",
    "descricao": "Desde ontem não consigo conectar na VPN da empresa.",
    "email_solicitante": "ana@empresa.com",
    "tags": ["vpn"],
}


def mostrar(passo: str, resposta) -> None:  # noqa: ANN001
    print(f"{passo:<34} -> {resposta.status_code} {resposta.text[:90]}")


mostrar("POST /tickets", client.post("/tickets", json=novo))
mostrar("GET /tickets", client.get("/tickets"))
mostrar("GET /tickets/1", client.get("/tickets/1"))
mostrar("GET /tickets/99 (não existe)", client.get("/tickets/99"))
mostrar(
    "PATCH /tickets/1/status",
    client.patch("/tickets/1/status", json={"status": "resolvido"}),
)
mostrar(
    "GET /tickets?status=resolvido",
    client.get("/tickets", params={"status": "resolvido"}),
)
mostrar(
    "POST e-mail inválido",
    client.post("/tickets", json={**novo, "email_solicitante": "x"}),
)
mostrar("DELETE /tickets/1", client.delete("/tickets/1"))
mostrar("DELETE /tickets/1 (de novo)", client.delete("/tickets/1"))
