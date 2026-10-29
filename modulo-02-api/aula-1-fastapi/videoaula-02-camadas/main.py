"""
VIDEOAULA 2 — API organizada em camadas (Routers e Services).

Execute:  uvicorn main:app --reload
"""

from fastapi import FastAPI
from routers import tickets

app = FastAPI(title="HelpDesk API")
app.include_router(tickets.router)
