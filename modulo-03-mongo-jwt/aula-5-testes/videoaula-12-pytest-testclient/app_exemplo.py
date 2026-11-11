"""
VIDEOAULA 12 — App mínimo para aprender Pytest + TestClient.
(Sem banco de dados: o foco é a ferramenta de testes.)
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="HelpDesk mínimo")

_chamados: dict[int, dict[str, str]] = {}


class ChamadoIn(BaseModel):
    titulo: str = Field(min_length=3)
    prioridade: str = "media"


@app.get("/")
def raiz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chamados", status_code=201)
def criar(dados: ChamadoIn) -> dict[str, int | str]:
    novo_id = len(_chamados) + 1
    _chamados[novo_id] = dados.model_dump()
    return {"id": novo_id, **dados.model_dump()}


@app.get("/chamados/{chamado_id}")
def buscar(chamado_id: int) -> dict[str, str]:
    if chamado_id not in _chamados:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    return _chamados[chamado_id]


def limpar() -> None:
    _chamados.clear()
