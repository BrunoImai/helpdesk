"""
AVALIAÇÃO DA AULA 4 — Mini Hands-on (GABARITO)
"""

from pydantic import BaseModel, EmailStr, Field, ValidationError


class TicketCreate(BaseModel):
    titulo: str = Field(min_length=5, max_length=100)
    descricao: str = Field(min_length=10)
    email_solicitante: EmailStr


dados_invalidos = {
    "titulo": "Sem internet no setor financeiro",
    "descricao": "A rede caiu às 9h e não voltou.",
    "email_solicitante": "ana.empresa.com",  # <- sem o @
}

dados_validos = {**dados_invalidos, "email_solicitante": "ana@empresa.com"}

if __name__ == "__main__":
    try:
        TicketCreate(**dados_invalidos)
    except ValidationError as erro:
        print("Dados rejeitados pela catraca:")
        for e in erro.errors():
            print(f"  - {e['loc'][0]}: {e['msg']}")

    ticket = TicketCreate(**dados_validos)
    print("\nDados válidos aceitos:", ticket)
