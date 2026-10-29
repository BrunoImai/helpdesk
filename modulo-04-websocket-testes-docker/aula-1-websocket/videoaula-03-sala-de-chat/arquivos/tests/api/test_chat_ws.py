"""TESTES DO CHAT EM TEMPO REAL (WebSocket) com o TestClient."""

from typing import Any

import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

EMAIL_CLIENTE = "cliente@empresa.com"


def url_cliente(ticket_id: str, email: str = EMAIL_CLIENTE) -> str:
    return f"/ws/tickets/{ticket_id}?email={email}"


def url_suporte(ticket_id: str, token: str) -> str:
    return f"/ws/tickets/{ticket_id}?token={token}"


def test_cliente_entra_recebe_historico_vazio_e_aviso(
    client: TestClient, ticket_criado: dict[str, Any]
) -> None:
    with client.websocket_connect(url_cliente(ticket_criado["id"])) as ws:
        assert ws.receive_json() == {"tipo": "historico", "mensagens": []}
        aviso = ws.receive_json()
        assert aviso["tipo"] == "sistema"
        assert EMAIL_CLIENTE in aviso["texto"]


def test_mensagem_enviada_volta_para_a_sala_e_fica_salva_no_banco(
    client: TestClient, auth_headers: dict[str, str], ticket_criado: dict[str, Any]
) -> None:
    with client.websocket_connect(url_cliente(ticket_criado["id"])) as ws:
        ws.receive_json()  # histórico
        ws.receive_json()  # "entrou no chat"

        ws.send_text("Alguém pode me ajudar com a VPN?")
        recebida = ws.receive_json()

    assert recebida["tipo"] == "mensagem"
    assert recebida["autor"] == EMAIL_CLIENTE
    assert recebida["texto"] == "Alguém pode me ajudar com a VPN?"

    # Persistência: a mensagem está no histórico do chamado
    ticket = client.get(f"/tickets/{ticket_criado['id']}", headers=auth_headers).json()
    assert [m["texto"] for m in ticket["mensagens"]] == [
        "Alguém pode me ajudar com a VPN?"
    ]


def test_cliente_e_suporte_conversam_na_mesma_sala(
    client: TestClient, token: str, ticket_criado: dict[str, Any]
) -> None:
    ticket_id = ticket_criado["id"]
    with client.websocket_connect(url_cliente(ticket_id)) as cliente:
        cliente.receive_json()  # histórico
        cliente.receive_json()  # "cliente entrou"

        with client.websocket_connect(url_suporte(ticket_id, token)) as suporte:
            suporte.receive_json()  # histórico
            assert "suporte" in suporte.receive_json()["texto"]  # "suporte entrou"
            assert "suporte" in cliente.receive_json()["texto"]  # cliente também vê

            suporte.send_text("Olá! Qual erro aparece?")

            para_suporte = suporte.receive_json()
            para_cliente = cliente.receive_json()

    assert para_suporte == para_cliente
    assert para_cliente["texto"] == "Olá! Qual erro aparece?"
    assert para_cliente["autor"].startswith("suporte")


def test_quem_entra_depois_recebe_o_historico(
    client: TestClient, ticket_criado: dict[str, Any]
) -> None:
    ticket_id = ticket_criado["id"]
    with client.websocket_connect(url_cliente(ticket_id)) as ws:
        ws.receive_json()
        ws.receive_json()
        ws.send_text("primeira mensagem")
        ws.receive_json()

    with client.websocket_connect(url_cliente(ticket_id)) as ws:
        historico = ws.receive_json()

    assert historico["tipo"] == "historico"
    assert [m["texto"] for m in historico["mensagens"]] == ["primeira mensagem"]


@pytest.mark.parametrize(
    "consulta",
    [
        "?email=intruso@outra.com",  # e-mail que não é do chamado
        "?token=lixo.lixo.lixo",  # token inválido
        "",  # nenhuma credencial
    ],
)
def test_acesso_negado_fecha_a_conexao(
    client: TestClient, ticket_criado: dict[str, Any], consulta: str
) -> None:
    with pytest.raises(WebSocketDisconnect) as erro:  # noqa: PT012
        with client.websocket_connect(
            f"/ws/tickets/{ticket_criado['id']}{consulta}"
        ) as ws:
            ws.receive_json()
    assert erro.value.code == 1008  # violação de política


def test_chamado_inexistente_fecha_a_conexao(client: TestClient) -> None:
    with pytest.raises(WebSocketDisconnect) as erro:  # noqa: PT012
        with client.websocket_connect(url_cliente("64b7f0c2a1b2c3d4e5f60718")) as ws:
            ws.receive_json()
    assert erro.value.code == 1008


def test_pagina_do_chat_e_servida(client: TestClient) -> None:
    resposta = client.get("/chat")
    assert resposta.status_code == 200
    assert "WebSocket" in resposta.text
