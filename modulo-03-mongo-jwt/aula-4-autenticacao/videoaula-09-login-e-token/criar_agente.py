"""
VIDEOAULA 9 — Cadastra um atendente no banco.

Execute:  python criar_agente.py "Ana Souza" ana@helpdesk.com
A senha é pedida no terminal (não aparece na tela).
"""

import asyncio
import getpass
import sys

from database import init_db
from models import Agente
from security import gerar_hash_senha


async def main(nome: str, email: str) -> None:
    senha = getpass.getpass("Senha do atendente (mín. 8 caracteres): ")
    if len(senha) < 8:
        sys.exit("Senha muito curta.")

    client = await init_db()
    try:
        if await Agente.find_one(Agente.email == email.lower()):
            sys.exit("Já existe um atendente com este e-mail.")
        agente = Agente(
            nome=nome, email=email.lower(), senha_hash=gerar_hash_senha(senha)
        )
        await agente.insert()
        print(f"Atendente criado: {agente.nome} <{agente.email}>")
        print(f"Hash guardado no banco: {agente.senha_hash[:20]}...")
    finally:
        client.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit('Uso: python criar_agente.py "Nome" email@dominio.com')
    asyncio.run(main(sys.argv[1], sys.argv[2]))
