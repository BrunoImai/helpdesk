"""
AVALIAÇÃO DA AULA 4 — Mini Hands-on (GABARITO)

Execute:  uvicorn gabarito:app --reload
"""

import asyncio

from fastapi import BackgroundTasks, FastAPI

app = FastAPI()

CHAMADOS = [
    {"id": 1, "titulo": "Sem internet", "status": "aberto"},
    {"id": 2, "titulo": "Impressora travada", "status": "resolvido"},
]


def registrar_acesso(rota: str) -> None:
    """Grava no log quem acessou."""
    print(f"Registrando acesso: {rota}")


@app.get("/tickets")
async def listar_tickets(background_tasks: BackgroundTasks) -> list[dict[str, object]]:
    await asyncio.sleep(1)  # simula uma consulta lenta ao banco (agora sem bloquear)
    background_tasks.add_task(registrar_acesso, "GET /tickets")
    return CHAMADOS
