"""VIDEOAULA 9 — Hash de senha (bcrypt) e geração/validação do JWT."""

from datetime import UTC, datetime, timedelta

import bcrypt
import jwt
from config import get_settings


def gerar_hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_senha(senha: str, senha_hash: str) -> bool:
    try:
        return bcrypt.checkpw(senha.encode("utf-8"), senha_hash.encode("utf-8"))
    except ValueError:
        return False


# >>> DEMONSTRAÇÃO: criando o "crachá" (JWT)
def criar_token_acesso(assunto: str) -> str:
    settings = get_settings()
    agora = datetime.now(UTC)
    payload = {
        "sub": assunto,  # quem é o dono do token (o e-mail do atendente)
        "iat": agora,  # quando foi emitido
        "exp": agora + timedelta(minutes=settings.access_token_expire_minutes),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def decodificar_token(token: str) -> str | None:
    """Devolve o `sub` do token ou None se for inválido/expirado."""
    settings = get_settings()
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.jwt_algorithm]
        )
    except jwt.InvalidTokenError:
        return None
    sub = payload.get("sub")
    return sub if isinstance(sub, str) else None
