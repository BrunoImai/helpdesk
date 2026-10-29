"""Demonstração das catracas do HelpDesk.

Execute (na pasta projeto-final):
    python -m scripts.validar_ticket
"""

from pydantic import ValidationError

from app.core.config import get_settings
from app.schemas.ticket import TicketCreate

CASOS: dict[str, dict[str, object]] = {
    "Chamado válido": {
        "titulo": "Sem acesso à VPN",
        "descricao": "Desde ontem não consigo conectar na VPN da empresa.",
        "email_solicitante": "Ana@Empresa.com",
        "tags": ["VPN", " rede "],
    },
    "E-mail incorreto": {
        "titulo": "Sem acesso à VPN",
        "descricao": "Desde ontem não consigo conectar na VPN da empresa.",
        "email_solicitante": "ana-empresa.com",
    },
    "E-mail descartável": {
        "titulo": "Sem acesso à VPN",
        "descricao": "Desde ontem não consigo conectar na VPN da empresa.",
        "email_solicitante": "ana@mailinator.com",
    },
}


def main() -> None:
    settings = get_settings()
    print(f"== {settings.app_name} (debug={settings.debug}) ==")
    for nome, dados in CASOS.items():
        print(f"\n[{nome}]")
        try:
            ticket = TicketCreate(**dados)  # type: ignore[arg-type]
            print("  ACEITO:", ticket.model_dump(mode="json"))
        except ValidationError as erro:
            for e in erro.errors():
                print(f"  REJEITADO -> {e['loc'][0]}: {e['msg']}")


if __name__ == "__main__":
    main()
