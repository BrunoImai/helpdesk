"""
AVALIAÇÃO DA AULA 4 — Mini Hands-on (ENUNCIADO)

A rota abaixo é SÍNCRONA. Faça duas mudanças:
  1. Torne a rota assíncrona (`async def`) e troque `time.sleep` por `await asyncio.sleep`.
  2. Depois de responder, registre o acesso usando `BackgroundTasks`
     (chame `registrar_acesso("GET /tickets")` em segundo plano).

Execute:  uvicorn enunciado_aluno:app --reload
"""

import time

from fastapi import FastAPI

app = FastAPI()

CHAMADOS = [
    {"id": 1, "titulo": "Sem internet", "status": "aberto"},
    {"id": 2, "titulo": "Impressora travada", "status": "resolvido"},
]


def registrar_acesso(rota: str) -> None:
    """Grava no log quem acessou. (Não precisa alterar esta função.)"""
    print(f"Registrando acesso: {rota}")


@app.get("/tickets")
def listar_tickets() -> list[dict[str, object]]:
    time.sleep(1)  # simula uma consulta lenta ao banco
    return CHAMADOS
