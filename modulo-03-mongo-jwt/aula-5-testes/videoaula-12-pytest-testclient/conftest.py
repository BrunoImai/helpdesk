"""
VIDEOAULA 12 — conftest.py: fixtures compartilhadas por todos os arquivos de teste.
O Pytest encontra este arquivo sozinho (não precisa importar).
"""

import app_exemplo
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Um TestClient novo e um "banco" limpo para CADA teste (testes independentes)."""
    app_exemplo.limpar()
    with TestClient(app_exemplo.app) as c:
        yield c
    app_exemplo.limpar()


@pytest.fixture
def chamado_criado(client):
    """Fixture que usa outra fixture: já deixa um chamado pronto."""
    resposta = client.post(
        "/chamados", json={"titulo": "VPN não conecta", "prioridade": "alta"}
    )
    return resposta.json()
