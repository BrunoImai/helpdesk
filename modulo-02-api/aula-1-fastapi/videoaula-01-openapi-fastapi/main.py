"""
VIDEOAULA 1 — Primeira API do HelpDesk e a documentação OpenAPI.

Execute:  uvicorn main:app --reload
"""

from fastapi import FastAPI

app = FastAPI(
    title="HelpDesk API",
    description="API de chamados da trilha *Dominando Python para Web*.",
    version="0.1.0",
)


# >>> DEMONSTRAÇÃO 1: a rota mais simples possível
@app.get("/")
def raiz() -> dict[str, str]:
    return {"mensagem": "HelpDesk no ar!"}


# >>> DEMONSTRAÇÃO 2: parâmetro de rota com tipo (vira validação + documentação)
@app.get("/tickets/{ticket_id}", summary="Consultar um chamado", tags=["Chamados"])
def consultar_ticket(ticket_id: int) -> dict[str, int | str]:
    """Devolve um chamado fictício. Teste com `/tickets/abc` e veja o erro 422."""
    return {"id": ticket_id, "titulo": "Sem internet", "status": "aberto"}


# >>> DEMONSTRAÇÃO 3: parâmetro de query com valor padrão
@app.get("/tickets", summary="Listar chamados", tags=["Chamados"])
def listar_tickets(status: str = "aberto", limit: int = 10) -> dict[str, object]:
    return {"filtro_status": status, "limite": limit, "itens": []}
