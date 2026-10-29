"""Regras de negócio dos atendentes (cadastro e autenticação)."""

from app.core.security import gerar_hash_senha, verificar_senha
from app.models.agente import Agente

# Hash de uma senha qualquer: usado para gastar o mesmo tempo mesmo quando o e-mail
# não existe (dificulta descobrir quais e-mails estão cadastrados).
_HASH_FALSO = gerar_hash_senha("senha-falsa-para-igualar-o-tempo")


class AgenteJaExisteError(Exception):
    pass


async def criar_agente(nome: str, email: str, senha: str) -> Agente:
    email = email.lower()
    if await Agente.find_one(Agente.email == email) is not None:
        raise AgenteJaExisteError(f"Já existe um atendente com o e-mail {email}")
    agente = Agente(nome=nome, email=email, senha_hash=gerar_hash_senha(senha))
    return await agente.insert()


async def autenticar(email: str, senha: str) -> Agente | None:
    """Devolve o atendente se e-mail e senha conferem; senão, None."""
    agente = await Agente.find_one(Agente.email == email.lower())
    if agente is None:
        verificar_senha(senha, _HASH_FALSO)
        return None
    if not verificar_senha(senha, agente.senha_hash) or not agente.ativo:
        return None
    return agente


async def buscar_por_email(email: str) -> Agente | None:
    return await Agente.find_one(Agente.email == email.lower())
