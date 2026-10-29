"""
VIDEOAULA 4 — Demonstração da leitura do .env.

Pré-requisito: `copy .env.example .env` (Windows) ou `cp .env.example .env`.
"""

from config import get_settings

# >>> DEMONSTRAÇÃO
settings = get_settings()

print(f"Aplicação : {settings.app_name}")
print(f"Debug     : {settings.debug} (tipo: {type(settings.debug).__name__})")
print(f"Mongo     : {settings.mongo_uri}")
# Nunca imprima segredos por completo (nem em logs):
print(f"Secret key: {settings.secret_key[:4]}{'*' * 12}")
