"""
VIDEOAULA 11 — Pirâmide de testes: um exemplo de cada camada.

Execute:   pytest exemplos -v
(O teste E2E só roda se você definir E2E_URL, ex.: com `uvicorn` rodando em outro terminal.)
"""

import os

import httpx
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# Código sob teste (no projeto real ficaria em app/)
# ---------------------------------------------------------------------------
def prazo_sla_horas(prioridade: str) -> int:
    """Regra de negócio pura: prazo de resposta (em horas) por prioridade."""
    prazos = {"alta": 4, "media": 24, "baixa": 72}
    if prioridade not in prazos:
        raise ValueError(f"Prioridade inválida: {prioridade}")
    return prazos[prioridade]


app = FastAPI()


@app.get("/sla/{prioridade}")
def rota_sla(prioridade: str) -> dict[str, int]:
    return {"horas": prazo_sla_horas(prioridade)}


# ---------------------------------------------------------------------------
# 1) BASE da pirâmide — UNIDADE: rápido, sem I/O, aos montes
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    ("prioridade", "esperado"), [("alta", 4), ("media", 24), ("baixa", 72)]
)
def test_unidade_prazo_sla(prioridade: str, esperado: int) -> None:
    assert prazo_sla_horas(prioridade) == esperado


def test_unidade_prioridade_invalida() -> None:
    with pytest.raises(ValueError, match="inválida"):
        prazo_sla_horas("urgentissima")


# ---------------------------------------------------------------------------
# 2) MEIO — INTEGRAÇÃO: várias peças juntas (rota + validação + serialização)
# ---------------------------------------------------------------------------
def test_integracao_rota_sla() -> None:
    client = TestClient(app, raise_server_exceptions=False)
    resposta = client.get("/sla/alta")
    assert resposta.status_code == 200
    assert resposta.json() == {"horas": 4}


# ---------------------------------------------------------------------------
# 3) TOPO — E2E: sistema real no ar (lento, frágil, poucos)
# ---------------------------------------------------------------------------
@pytest.mark.skipif(
    not os.getenv("E2E_URL"), reason="defina E2E_URL (ex.: http://127.0.0.1:8000)"
)
def test_e2e_api_no_ar() -> None:
    resposta = httpx.get(os.environ["E2E_URL"] + "/", timeout=5)
    assert resposta.status_code == 200
