"""
VIDEOAULA 3 — Qual Python estou usando?

Rode antes e depois de ativar o ambiente virtual e compare a saída:
    python mostra_ambiente.py
"""

import sys
from importlib import metadata

# >>> DEMONSTRAÇÃO
print(f"Python em uso : {sys.executable}")
print(f"Versão        : {sys.version.split()[0]}")
print(f"Prefixo       : {sys.prefix}")

# Dentro de um venv, sys.prefix é diferente de sys.base_prefix
dentro_de_venv = sys.prefix != sys.base_prefix
print(f"Dentro de venv: {'SIM' if dentro_de_venv else 'NÃO'}")

for pacote in ("fastapi", "pydantic"):
    try:
        print(f"{pacote:<14}: {metadata.version(pacote)}")
    except metadata.PackageNotFoundError:
        print(f"{pacote:<14}: não instalado neste ambiente")
