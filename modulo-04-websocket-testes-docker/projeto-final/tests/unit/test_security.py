"""TESTES DE UNIDADE: funções puras de segurança (rápidos, sem banco e sem HTTP)."""

from datetime import timedelta

import jwt

from app.core.config import get_settings
from app.core.security import (
    criar_token_acesso,
    decodificar_token,
    gerar_hash_senha,
    verificar_senha,
)


def test_hash_nao_guarda_a_senha_em_texto_puro() -> None:
    hash_ = gerar_hash_senha("MinhaSenha@123")
    assert "MinhaSenha@123" not in hash_
    assert hash_.startswith("$2b$")  # formato bcrypt


def test_mesma_senha_gera_hashes_diferentes_por_causa_do_sal() -> None:
    assert gerar_hash_senha("abc12345") != gerar_hash_senha("abc12345")


def test_verificar_senha_correta_e_incorreta() -> None:
    hash_ = gerar_hash_senha("senha-certa")
    assert verificar_senha("senha-certa", hash_) is True
    assert verificar_senha("senha-errada", hash_) is False


def test_verificar_senha_com_hash_malformado_nao_levanta_erro() -> None:
    assert verificar_senha("qualquer", "isto-nao-e-um-hash") is False


def test_token_valido_devolve_o_assunto() -> None:
    token = criar_token_acesso("ana@helpdesk.com")
    assert decodificar_token(token) == "ana@helpdesk.com"


def test_token_expirado_e_rejeitado() -> None:
    token = criar_token_acesso("ana@helpdesk.com", expira_em=timedelta(seconds=-1))
    assert decodificar_token(token) is None


def test_token_adulterado_e_rejeitado() -> None:
    cabecalho, corpo, assinatura = criar_token_acesso("ana@helpdesk.com").split(".")
    adulterado = f"{cabecalho}.{corpo}x.{assinatura}"
    assert decodificar_token(adulterado) is None


def test_token_assinado_com_outra_chave_e_rejeitado() -> None:
    settings = get_settings()
    falso = jwt.encode(
        {"sub": "ana@helpdesk.com"},
        "outra-chave-com-mais-de-trinta-e-dois-caracteres",
        algorithm=settings.jwt_algorithm,
    )
    assert decodificar_token(falso) is None


def test_lixo_no_lugar_do_token_e_rejeitado() -> None:
    assert decodificar_token("isto-nao-e-um-jwt") is None
