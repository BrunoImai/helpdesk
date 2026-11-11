"""VIDEOAULA 12 — Primeiros testes: arrange / act / assert."""

import pytest


def test_raiz_responde_ok(client):
    resposta = client.get("/")  # act
    assert resposta.status_code == 200  # assert
    assert resposta.json() == {"status": "ok"}


def test_criar_chamado(client):
    resposta = client.post("/chamados", json={"titulo": "Impressora parou"})
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["id"] == 1
    assert corpo["prioridade"] == "media"  # valor padrão


def test_buscar_chamado_existente(client, chamado_criado):
    resposta = client.get(f"/chamados/{chamado_criado['id']}")
    assert resposta.status_code == 200
    assert resposta.json()["titulo"] == "VPN não conecta"


def test_buscar_chamado_inexistente(client):
    resposta = client.get("/chamados/999")
    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Chamado não encontrado"


@pytest.mark.parametrize("titulo", ["", "ab"])
def test_titulo_curto_demais_e_rejeitado(client, titulo):
    resposta = client.post("/chamados", json={"titulo": titulo})
    assert resposta.status_code == 422  # validação do Pydantic


# >>> DEMONSTRAÇÃO: remova o "x" do nome da função e veja o teste falhar de propósito
def x_test_falha_de_proposito(client):
    assert client.get("/").status_code == 500
