"""
GABARITO — Mini hands-on da Aula 5: teste que verifica o 401 Unauthorized sem token.

Execute:  pytest gabarito.py -v
(Não precisa de banco: `TestClient(app)` SEM `with` não executa o lifespan, e a autenticação
 recusa a requisição antes de qualquer consulta ao MongoDB.)
"""

import os
import sys
from pathlib import Path

# Variáveis exigidas pela configuração, definidas ANTES de importar a aplicação
os.environ.setdefault("SECRET_KEY", "chave-somente-para-testes-0123456789abcdef")
os.environ.setdefault("MONGO_URI", "mongodb://banco-que-nunca-sera-usado:27017")

# Torna o pacote `app` do projeto-final importável a partir desta pasta
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "projeto-final"))

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

client = TestClient(app)


def test_listar_chamados_sem_token_devolve_401() -> None:
    resposta = client.get("/tickets")

    assert resposta.status_code == 401
    assert resposta.headers["www-authenticate"] == "Bearer"


def test_token_invalido_tambem_devolve_401() -> None:
    resposta = client.get("/tickets", headers={"Authorization": "Bearer token-invalido"})

    assert resposta.status_code == 401


@pytest.mark.parametrize("url", ["/tickets/resumo", "/tickets/resolvidos", "/auth/eu"])
def test_outras_rotas_do_suporte_tambem_exigem_token(url: str) -> None:
    assert client.get(url).status_code == 401
