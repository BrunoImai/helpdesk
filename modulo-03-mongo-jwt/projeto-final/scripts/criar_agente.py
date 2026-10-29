"""Cria um atendente no banco (os atendentes não se cadastram sozinhos pela API).

Execute (na pasta projeto-final, com o .env preenchido):
    python -m scripts.criar_agente "Ana Souza" ana@helpdesk.com
A senha é pedida no terminal (não aparece na tela nem no histórico).
"""

import asyncio
import getpass
import sys

from app.core.database import init_db
from app.services.agente_service import AgenteJaExisteError, criar_agente


async def main(nome: str, email: str) -> None:
    senha = getpass.getpass("Senha do atendente (mín. 8 caracteres): ")
    if len(senha) < 8:
        sys.exit("Senha muito curta.")

    client = await init_db()
    try:
        agente = await criar_agente(nome, email, senha)
        print(f"Atendente criado: {agente.nome} <{agente.email}> (id {agente.id})")
    except AgenteJaExisteError as erro:
        sys.exit(str(erro))
    finally:
        if client is not None:
            client.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit('Uso: python -m scripts.criar_agente "Nome" email@dominio.com')
    asyncio.run(main(sys.argv[1], sys.argv[2]))
