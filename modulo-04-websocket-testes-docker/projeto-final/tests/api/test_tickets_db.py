"""TESTES DE INTEGRAÇÃO: rotas + serviço + Beanie, usando o MongoDB falso em memória."""

from typing import Any

from fastapi.testclient import TestClient

ID_INEXISTENTE = "64b7f0c2a1b2c3d4e5f60718"


def test_criar_e_consultar_chamado(
    client: TestClient, auth_headers: dict[str, str], ticket_criado: dict[str, Any]
) -> None:
    assert ticket_criado["status"] == "aberto"
    assert ticket_criado["id"]

    resposta = client.get(f"/tickets/{ticket_criado['id']}", headers=auth_headers)

    assert resposta.status_code == 200
    assert resposta.json()["titulo"] == "Sem acesso à VPN"


def test_listar_fila_mais_recente_primeiro(
    client: TestClient, auth_headers: dict[str, str], ticket_payload: dict[str, Any]
) -> None:
    client.post("/tickets", json={**ticket_payload, "titulo": "Primeiro chamado"})
    client.post("/tickets", json={**ticket_payload, "titulo": "Segundo chamado"})

    resposta = client.get("/tickets", headers=auth_headers)

    assert resposta.status_code == 200
    assert [t["titulo"] for t in resposta.json()] == [
        "Segundo chamado",
        "Primeiro chamado",
    ]


def test_filtrar_por_prioridade_e_paginar(
    client: TestClient, auth_headers: dict[str, str], ticket_payload: dict[str, Any]
) -> None:
    descricao_longa = "Sistema inteiro fora do ar, ninguém consegue trabalhar hoje."
    for i in range(3):
        client.post(
            "/tickets",
            json={
                **ticket_payload,
                "titulo": f"Chamado urgente {i}",
                "prioridade": "alta",
                "descricao": descricao_longa,
            },
        )
    client.post("/tickets", json=ticket_payload)  # prioridade media

    altas = client.get("/tickets?prioridade=alta", headers=auth_headers).json()
    primeira_pagina = client.get("/tickets?limit=2", headers=auth_headers).json()

    assert len(altas) == 3
    assert len(primeira_pagina) == 2


def test_alterar_status_e_listar_resolvidos(
    client: TestClient, auth_headers: dict[str, str], ticket_criado: dict[str, Any]
) -> None:
    ticket_id = ticket_criado["id"]
    assert client.get("/tickets/resolvidos", headers=auth_headers).json() == []

    resposta = client.patch(
        f"/tickets/{ticket_id}/status",
        json={"status": "resolvido"},
        headers=auth_headers,
    )

    assert resposta.status_code == 200
    assert resposta.json()["status"] == "resolvido"
    assert resposta.json()["atualizado_em"] is not None
    resolvidos = client.get("/tickets/resolvidos", headers=auth_headers).json()
    assert [t["id"] for t in resolvidos] == [ticket_id]


def test_status_invalido_devolve_422(
    client: TestClient, auth_headers: dict[str, str], ticket_criado: dict[str, Any]
) -> None:
    resposta = client.patch(
        f"/tickets/{ticket_criado['id']}/status",
        json={"status": "inventado"},
        headers=auth_headers,
    )
    assert resposta.status_code == 422


def test_substituir_chamado(
    client: TestClient, auth_headers: dict[str, str], ticket_criado: dict[str, Any]
) -> None:
    novos_dados = {
        "titulo": "Título totalmente novo",
        "descricao": "Descrição atualizada pelo suporte do HelpDesk.",
        "email_solicitante": "cliente@empresa.com",
    }
    resposta = client.put(
        f"/tickets/{ticket_criado['id']}", json=novos_dados, headers=auth_headers
    )
    assert resposta.status_code == 200
    assert resposta.json()["titulo"] == "Título totalmente novo"


def test_apagar_chamado(
    client: TestClient, auth_headers: dict[str, str], ticket_criado: dict[str, Any]
) -> None:
    url = f"/tickets/{ticket_criado['id']}"

    assert client.delete(url, headers=auth_headers).status_code == 204
    assert client.get(url, headers=auth_headers).status_code == 404


def test_chamado_inexistente_devolve_404_com_mensagem_humanizada(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    resposta = client.get(f"/tickets/{ID_INEXISTENTE}", headers=auth_headers)

    assert resposta.status_code == 404
    assert ID_INEXISTENTE in resposta.json()["detail"]
    assert "não encontrado" in resposta.json()["detail"]


def test_resumo_por_status(
    client: TestClient, auth_headers: dict[str, str], ticket_payload: dict[str, Any]
) -> None:
    for _ in range(2):
        client.post("/tickets", json=ticket_payload)
    resolvido = client.post("/tickets", json=ticket_payload).json()
    client.patch(
        f"/tickets/{resolvido['id']}/status",
        json={"status": "resolvido"},
        headers=auth_headers,
    )

    resposta = client.get("/tickets/resumo", headers=auth_headers)

    assert resposta.status_code == 200
    assert {r["status"]: r["total"] for r in resposta.json()} == {
        "aberto": 2,
        "resolvido": 1,
    }


def test_banco_comeca_vazio_em_cada_teste(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    """Prova do isolamento: nenhum chamado dos outros testes aparece aqui."""
    assert client.get("/tickets", headers=auth_headers).json() == []
