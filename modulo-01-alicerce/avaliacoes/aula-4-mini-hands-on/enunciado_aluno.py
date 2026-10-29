"""
AVALIAÇÃO DA AULA 4 — Mini Hands-on (ENUNCIADO)

Complete os TODO:
1. Crie o modelo `TicketCreate` com os campos:
   - titulo: texto, entre 5 e 100 caracteres
   - descricao: texto, no mínimo 10 caracteres
   - email_solicitante: e-mail válido
2. Valide o dicionário `dados_invalidos` e mostre o erro na tela.
"""

# TODO: importe BaseModel, EmailStr, Field e ValidationError do pydantic


# TODO: escreva a classe TicketCreate


dados_invalidos = {
    "titulo": "Sem internet no setor financeiro",
    "descricao": "A rede caiu às 9h e não voltou.",
    "email_solicitante": "ana.empresa.com",  # <- sem o @
}

# TODO: tente criar TicketCreate(**dados_invalidos) dentro de um try/except
#       e imprima a mensagem do erro.
