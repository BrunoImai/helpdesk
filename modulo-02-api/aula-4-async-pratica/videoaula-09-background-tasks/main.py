"""
VIDEOAULA 9 — BackgroundTasks: enviando e-mail sem travar a resposta.

Execute:  uvicorn main:app --reload
"""

import asyncio
import logging

from fastapi import BackgroundTasks, FastAPI, status
from pydantic import BaseModel, EmailStr, Field

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")
log = logging.getLogger("helpdesk")

app = FastAPI(title="HelpDesk API — Videoaula 9")


class TicketCreate(BaseModel):
    titulo: str = Field(min_length=5, max_length=100)
    email_solicitante: EmailStr


async def enviar_email(destino: str, titulo: str) -> None:
    """Simula um envio de e-mail lento (2 segundos)."""
    log.info("Enviando e-mail para %s ...", destino)
    await asyncio.sleep(2)
    log.info("E-mail enviado para %s: 'Recebemos seu chamado: %s'", destino, titulo)


# >>> DEMONSTRAÇÃO 1: SEM background — o cliente espera o e-mail terminar
@app.post("/tickets-lento", status_code=status.HTTP_201_CREATED, tags=["Demo"])
async def criar_lento(dados: TicketCreate) -> dict[str, str]:
    await enviar_email(dados.email_solicitante, dados.titulo)  # <- 2 s de espera
    return {"mensagem": "Chamado criado", "titulo": dados.titulo}


# >>> DEMONSTRAÇÃO 2: COM background — resposta imediata, e-mail depois
@app.post("/tickets", status_code=status.HTTP_201_CREATED, tags=["Chamados"])
async def criar(
    dados: TicketCreate, background_tasks: BackgroundTasks
) -> dict[str, str]:
    background_tasks.add_task(enviar_email, dados.email_solicitante, dados.titulo)
    return {"mensagem": "Chamado criado. Você receberá um e-mail de confirmação."}
