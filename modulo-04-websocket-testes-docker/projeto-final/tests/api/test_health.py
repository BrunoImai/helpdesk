"""PRIMEIRO TESTE COM TestClient (Videoaula 5).

`TestClient(app)` SEM `with` não executa o lifespan: não conecta no banco.
É ideal para rotas que não precisam de dados.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_raiz_responde_ok() -> None:
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "ok"


def test_rota_inexistente_devolve_404() -> None:
    assert client.get("/nao-existe").status_code == 404


def test_swagger_e_openapi_estao_disponiveis() -> None:
    assert client.get("/docs").status_code == 200
    esquema = client.get("/openapi.json").json()
    assert esquema["info"]["title"] == "HelpDesk API"
    assert "/tickets" in esquema["paths"]
