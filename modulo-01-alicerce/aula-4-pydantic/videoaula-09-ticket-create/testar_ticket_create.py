"""
VIDEOAULA 9 — Testando o contrato TicketCreate.

Execute:  python testar_ticket_create.py
"""

from pydantic import ValidationError
from ticket_create import TicketCreate


def mostrar_erros(erro: ValidationError) -> None:
    for e in erro.errors():
        campo = ".".join(str(parte) for parte in e["loc"])
        print(f"  - {campo}: {e['msg']} (tipo: {e['type']})")


# 1. Dados válidos
print("=== Chamado válido ===")
ok = TicketCreate(
    titulo="Sem acesso à VPN",
    descricao="Desde ontem não consigo conectar na VPN da empresa.",
    email_solicitante="ana@empresa.com",
)
print(ok)
print(ok.model_dump_json(indent=2))

# 2. Título curto demais + e-mail sem @ + prioridade inexistente
print("\n=== Chamado inválido ===")
try:
    TicketCreate(
        titulo="VPN",
        descricao="curto",
        email_solicitante="ana-empresa.com",
        prioridade="urgentissima",
    )
except ValidationError as erro:
    print(f"{erro.error_count()} erros encontrados:")
    mostrar_erros(erro)

# 3. Campo obrigatório ausente
print("\n=== Campo obrigatório ausente ===")
try:
    TicketCreate.model_validate({"titulo": "Sem internet no setor"})
except ValidationError as erro:
    mostrar_erros(erro)
