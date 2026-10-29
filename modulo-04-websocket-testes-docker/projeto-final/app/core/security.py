"""Segurança: hash de senhas (bcrypt) e tokens JWT."""

from datetime import UTC, datetime, timedelta

import bcrypt
import jwt

from app.core.config import get_settings


# ---------------------------------------------------------------------------
# Senhas: guardamos apenas o HASH (de mão única), nunca a senha
# ---------------------------------------------------------------------------
def gerar_hash_senha(senha: str) -> str:
    """Gera o hash bcrypt (o 'salt' aleatório já vem embutido no resultado)."""
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_senha(senha: str, senha_hash: str) -> bool:
    try:
        return bcrypt.checkpw(senha.encode("utf-8"), senha_hash.encode("utf-8"))
    except ValueError:  # hash malformado
        return False


# ---------------------------------------------------------------------------
# Tokens JWT
# ---------------------------------------------------------------------------
def criar_token_acesso(assunto: str, expira_em: timedelta | None = None) -> str:
    """Cria um JWT assinado. `assunto` (claim `sub`) identifica o atendente."""
    settings = get_settings()
    agora = datetime.now(UTC)
    expira_em = expira_em or timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": assunto, "iat": agora, "exp": agora + expira_em}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def decodificar_token(token: str) -> str | None:
    """Valida assinatura e validade. Devolve o `sub` ou None se o token for inválido."""
    settings = get_settings()
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.jwt_algorithm]
        )
    except jwt.InvalidTokenError:  # inclui expirado e assinatura inválida
        return None
    sub = payload.get("sub")
    return sub if isinstance(sub, str) else None
