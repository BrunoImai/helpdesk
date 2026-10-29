"""
VIDEOAULA 8 — Serialização: traduzindo JSON para Python e vice-versa.

Execute:  python serializacao.py
"""

import json
from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel

# ---------------------------------------------------------------------------
# 1. Com o módulo json padrão
# ---------------------------------------------------------------------------
print("=== 1. json padrão ===")
chamado_dict = {"id": 1, "titulo": "Sem internet", "urgente": True, "responsavel": None}

texto_json = json.dumps(chamado_dict)  # Python -> JSON (str)
print(texto_json)  # {"id": 1, ..., "urgente": true, "responsavel": null}

de_volta = json.loads(texto_json)  # JSON (str) -> Python (dict)
print(de_volta, type(de_volta))

# Limitação: tipos "ricos" não são serializáveis
try:
    json.dumps({"criado_em": datetime.now()})
except TypeError as erro:
    print(f"Erro esperado: {erro}")


# ---------------------------------------------------------------------------
# 2. Com Pydantic
# ---------------------------------------------------------------------------
print("\n=== 2. Pydantic ===")


class Status(StrEnum):
    ABERTO = "aberto"
    RESOLVIDO = "resolvido"


class Chamado(BaseModel):
    id: int
    titulo: str
    status: Status = Status.ABERTO
    criado_em: datetime
    responsavel: str | None = None


chamado = Chamado(id=1, titulo="Sem internet", criado_em=datetime(2026, 1, 15, 9, 30))

# Objeto -> dict (ainda com objetos Python)
print(chamado.model_dump())

# Objeto -> dict "seguro para JSON" (datetime e Enum viram texto)
print(chamado.model_dump(mode="json"))

# Objeto -> texto JSON
json_texto = chamado.model_dump_json(indent=2)
print(json_texto)

# JSON -> objeto, já validando e convertendo tipos
entrada = '{"id": "10", "titulo": "VPN caiu", "criado_em": "2026-02-01T08:00:00"}'
novo = Chamado.model_validate_json(entrada)
print(novo)
print(f"id virou {type(novo.id).__name__}: {novo.id}")  # "10" -> 10 (int)
print(f"criado_em virou {type(novo.criado_em).__name__}")

# dict -> objeto
a_partir_de_dict = Chamado.model_validate(
    {"id": 2, "titulo": "Impressora", "criado_em": "2026-03-01T10:00:00"}
)
print(a_partir_de_dict.status)  # valor padrão aplicado
