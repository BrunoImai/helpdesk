"""
VIDEOAULA 3 — Testa a connection string do .env ANTES de subir a API.

Execute:  python testar_conexao.py
"""

import asyncio
import sys

from config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError


async def main() -> None:
    settings = get_settings()
    # Mostra só o "host", nunca usuário e senha
    host = settings.mongo_uri.split("@")[-1]
    print(f"Tentando conectar em: {host}")

    client = AsyncIOMotorClient(settings.mongo_uri, serverSelectionTimeoutMS=5000)
    try:
        await client.admin.command("ping")
        print("Conexão OK! O MongoDB respondeu ao ping.")
    except PyMongoError as erro:
        print(f"Falha na conexão: {type(erro).__name__}")
        print("Verifique: MONGO_URI no .env, usuário/senha e o acesso por IP no Atlas.")
        sys.exit(1)
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(main())
