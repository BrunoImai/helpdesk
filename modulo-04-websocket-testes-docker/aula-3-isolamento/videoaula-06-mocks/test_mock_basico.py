"""
VIDEOAULA 6 — Mocks na prática (auto-contido: roda sem banco, sem internet, sem projeto).

Execute:  pytest test_mock_basico.py -v
Requer:   pip install pytest pytest-asyncio
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


# ---------------------------------------------------------------------------
# Código sob teste (no HelpDesk seria o service + o envio de e-mail)
# ---------------------------------------------------------------------------
async def enviar_email(destino: str, assunto: str) -> None:
    await asyncio.sleep(2)  # simula um servidor SMTP lento
    print(f"E-mail real enviado para {destino}")


async def abrir_chamado(titulo: str, email: str) -> dict[str, str]:
    await enviar_email(email, f"Chamado aberto: {titulo}")
    return {"titulo": titulo, "email": email}


def consultar_cliente(api) -> str:
    return api.buscar("cliente-1")["nome"].upper()


# ---------------------------------------------------------------------------
# 1) MagicMock: um objeto "falso" que aceita qualquer chamada e devolve o que você mandar
# ---------------------------------------------------------------------------
def test_magicmock_devolve_valor_combinado() -> None:
    api_falsa = MagicMock()
    api_falsa.buscar.return_value = {"nome": "Ana"}

    assert consultar_cliente(api_falsa) == "ANA"
    api_falsa.buscar.assert_called_once_with("cliente-1")  # verifica COMO foi usado


# ---------------------------------------------------------------------------
# 2) patch: troca uma função real por um mock SÓ dentro do teste
# ---------------------------------------------------------------------------
async def test_patch_evita_envio_real_de_email() -> None:
    # `patch` troca o nome ONDE ele é usado (neste módulo), não onde foi definido
    with patch(f"{__name__}.enviar_email", new=AsyncMock()) as email_falso:
        resultado = await abrir_chamado("VPN fora do ar", "ana@empresa.com")

    assert resultado["titulo"] == "VPN fora do ar"
    email_falso.assert_awaited_once_with(
        "ana@empresa.com", "Chamado aberto: VPN fora do ar"
    )


# ---------------------------------------------------------------------------
# 3) Mock que FALHA: testa o caminho de erro sem precisar derrubar nada de verdade
# ---------------------------------------------------------------------------
async def test_erro_no_envio_de_email_propaga() -> None:
    falha = AsyncMock(side_effect=ConnectionError("SMTP fora do ar"))

    with patch(f"{__name__}.enviar_email", new=falha), pytest.raises(ConnectionError):
        await abrir_chamado("Teste", "ana@empresa.com")


# ---------------------------------------------------------------------------
# >>> DEMONSTRAÇÃO: sem o patch, o teste fica LENTO (2 s) — rode e compare os tempos
# ---------------------------------------------------------------------------
@pytest.mark.skip(reason="demonstração: remova esta linha para ver o teste lento (2 s)")
async def test_sem_mock_e_lento() -> None:
    await abrir_chamado("Lento", "ana@empresa.com")
