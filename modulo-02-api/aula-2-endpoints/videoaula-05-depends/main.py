"""
VIDEOAULA 5 — Injeção de dependências com Depends.

Execute:  uvicorn main:app --reload
"""

from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Query

app = FastAPI(title="HelpDesk API — Videoaula 5")


# ---------------------------------------------------------------------------
# 1. Dependência como FUNÇÃO: parâmetros comuns de paginação
# ---------------------------------------------------------------------------
def paginacao(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
) -> dict[str, int]:
    return {"skip": skip, "limit": limit}


# ---------------------------------------------------------------------------
# 2. Dependência como CLASSE + alias reutilizável com Annotated
# ---------------------------------------------------------------------------
class Paginacao:
    def __init__(
        self,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=50)] = 10,
    ) -> None:
        self.skip = skip
        self.limit = limit


PaginacaoDep = Annotated[Paginacao, Depends()]


# ---------------------------------------------------------------------------
# 3. Dependência de SERVIÇO: um recurso compartilhado entre as rotas
# ---------------------------------------------------------------------------
class TicketService:
    def __init__(self) -> None:
        self.tickets = [
            {"id": i, "titulo": f"Chamado de exemplo {i}", "status": "aberto"}
            for i in range(1, 8)
        ]

    def listar(self, skip: int, limit: int) -> list[dict[str, object]]:
        return self.tickets[skip : skip + limit]

    def buscar(self, ticket_id: int) -> dict[str, object] | None:
        return next((t for t in self.tickets if t["id"] == ticket_id), None)


_servico_unico = TicketService()


def get_ticket_service() -> TicketService:
    return _servico_unico


ServiceDep = Annotated[TicketService, Depends(get_ticket_service)]


@app.get("/tickets", tags=["Chamados"])
def listar(paginacao: PaginacaoDep, service: ServiceDep) -> list[dict[str, object]]:
    return service.listar(paginacao.skip, paginacao.limit)


@app.get("/tickets/{ticket_id}", tags=["Chamados"])
def obter(ticket_id: int, service: ServiceDep) -> dict[str, object]:
    ticket = service.buscar(ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    return ticket


# ---------------------------------------------------------------------------
# 4. Dependência que PROTEGE rotas (aperitivo da autenticação do Módulo 3)
# ---------------------------------------------------------------------------
def verificar_chave(x_api_key: Annotated[str | None, Header()] = None) -> None:
    if x_api_key != "segredo-do-helpdesk":
        raise HTTPException(status_code=401, detail="Chave de API ausente ou inválida")


@app.get("/admin/resumo", dependencies=[Depends(verificar_chave)], tags=["Admin"])
def resumo(service: ServiceDep) -> dict[str, int]:
    return {"total_chamados": len(service.tickets)}


# ---------------------------------------------------------------------------
# 5. Dependências que dependem de outras dependências
# ---------------------------------------------------------------------------
def contexto_da_lista(
    paginacao: PaginacaoDep, service: ServiceDep
) -> dict[str, object]:
    return {
        "itens": service.listar(paginacao.skip, paginacao.limit),
        "pagina_de": paginacao.skip,
    }


@app.get("/tickets-com-contexto", tags=["Chamados"])
def listar_com_contexto(
    contexto: Annotated[dict[str, object], Depends(contexto_da_lista)],
) -> dict[str, object]:
    return contexto
