"""
VIDEOAULA 10 — Testando os validadores customizados.

Execute:  python testar_validadores.py
"""

from pydantic import ValidationError
from ticket_create import TicketCreate


def tentar(rotulo: str, **dados: object) -> None:
    print(f"\n--- {rotulo} ---")
    try:
        ticket = TicketCreate(**dados)  # type: ignore[arg-type]
        print("ACEITO:", ticket.model_dump())
    except ValidationError as erro:
        for e in erro.errors():
            campo = ".".join(str(p) for p in e["loc"]) or "(modelo)"
            print(f"REJEITADO -> {campo}: {e['msg']}")


base = {
    "titulo": "Sem acesso à VPN",
    "descricao": "Desde ontem não consigo conectar na VPN da empresa.",
    "email_solicitante": "Ana@Empresa.com",
}

tentar("1. Válido (e-mail é normalizado para minúsculas)", **base)
tentar("2. E-mail descartável", **{**base, "email_solicitante": "joao@mailinator.com"})
tentar("3. E-mail malformado", **{**base, "email_solicitante": "joao-sem-arroba.com"})
tentar(
    "4. Título com espaços extras", **{**base, "titulo": "   Sem   acesso   à   VPN  "}
)
tentar("5. Tags sujas", **{**base, "tags": [" VPN ", "rede", "vpn", ""]})
tentar(
    "6. Prioridade ALTA com descrição curta",
    **{**base, "descricao": "Muito urgente!!!", "prioridade": "alta"},
)
