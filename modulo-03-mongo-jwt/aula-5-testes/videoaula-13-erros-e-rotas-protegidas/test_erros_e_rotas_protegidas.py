"""
VIDEOAULA 13 — Testando erros e rotas protegidas.

Testa a API do `projeto-final` do Módulo 3 SEM banco de dados:
  - dados inválidos            -> 422 (o Pydantic barra antes de chegar no MongoDB)
  - rota protegida sem token   -> 401
  - token inválido             -> 401

Execute (dentro desta pasta, com o ambiente do projeto-final ativo):
    pytest test_erros_e_rotas_protegidas.py -v
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

# Sem `with`: o lifespan não roda, então nada tenta conectar no banco
client = TestClient(app)

CHAMADO_VALIDO = {
    "titulo": "Sem acesso à VPN",
    "descricao": "Desde ontem não consigo conectar na VPN da empresa.",
    "email_solicitante": "cliente@empresa.com",
}


# ---------------------------------------------------------------------------
# >>> DEMONSTRAÇÃO 1: caminho de erro com dados inválidos (422)
# ---------------------------------------------------------------------------
def test_email_invalido_devolve_422() -> None:
    dados = {**CHAMADO_VALIDO, "email_solicitante": "isto-nao-e-um-email"}

    resposta = client.post("/tickets", json=dados)

    assert resposta.status_code == 422


def test_titulo_com_tipo_errado_devolve_422() -> None:
    # `titulo` deve ser texto: um número no lugar é rejeitado pelo Pydantic.
    dados = {**CHAMADO_VALIDO, "titulo": 12345}

    resposta = client.post("/tickets", json=dados)

    assert resposta.status_code == 422


# ---------------------------------------------------------------------------
# >>> DEMONSTRAÇÃO 2: rota protegida sem token (401)
# ---------------------------------------------------------------------------
def test_listar_chamados_sem_token_devolve_401() -> None:
    resposta = client.get("/tickets")

    assert resposta.status_code == 401
    assert resposta.headers["www-authenticate"] == "Bearer"


def test_token_invalido_devolve_401() -> None:
    resposta = client.get("/tickets", headers={"Authorization": "Bearer token-falso"})

    assert resposta.status_code == 401


@pytest.mark.parametrize("url", ["/tickets/resumo", "/tickets/resolvidos", "/auth/eu"])
def test_outras_rotas_do_suporte_exigem_token(url: str) -> None:
    assert client.get(url).status_code == 401
