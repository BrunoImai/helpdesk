"""Configuração dos testes do HelpDesk.

As variáveis abaixo são definidas ANTES de importar a aplicação, para que os testes
nunca dependam do seu `.env` nem de um banco de dados real.
"""

import os

os.environ.setdefault("SECRET_KEY", "chave-somente-para-testes-0123456789abcdef")
os.environ.setdefault("MONGO_URI", "mongodb://banco-que-nunca-sera-usado:27017")
os.environ.setdefault("MONGO_DB_NAME", "helpdesk_testes")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


@pytest.fixture
def client() -> TestClient:
    """Cliente de testes SEM `with`: o lifespan não roda, então não conecta no banco.

    Serve para testar tudo o que é decidido ANTES de tocar no MongoDB:
    saúde da API, validação de dados (422) e autenticação (401).
    """
    return TestClient(app)
