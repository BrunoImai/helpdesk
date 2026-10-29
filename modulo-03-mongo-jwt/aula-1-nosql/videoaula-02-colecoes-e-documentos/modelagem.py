"""
VIDEOAULA 2 — Modelando o chamado como documento.

Mensagens: EMBUTIDAS no chamado (sempre lidas junto, pertencem só a ele).
Atendente: REFERENCIADO por id (existe por conta própria e atende vários chamados).

Execute:  python modelagem.py
"""

import json
from datetime import UTC, datetime

from pydantic import BaseModel, Field


class Mensagem(BaseModel):
    autor: str
    texto: str
    enviada_em: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Chamado(BaseModel):
    titulo: str
    descricao: str
    prioridade: str = "media"
    status: str = "aberto"
    tags: list[str] = Field(default_factory=list)
    agente_id: str | None = None  # referência (guarda só o id do atendente)
    mensagens: list[Mensagem] = Field(default_factory=list)  # embutido


if __name__ == "__main__":
    chamado = Chamado(
        titulo="VPN não conecta",
        descricao="Desde ontem a VPN retorna erro 809.",
        prioridade="alta",
        tags=["vpn", "rede"],
        agente_id="64b7ef11a1b2c3d4e5f60001",
    )
    chamado.mensagens.append(Mensagem(autor="ana@empresa.com", texto="Não conecto."))
    chamado.mensagens.append(Mensagem(autor="suporte", texto="Qual erro aparece?"))

    print(json.dumps(chamado.model_dump(mode="json"), indent=2, ensure_ascii=False))
    print(f"\nO chamado tem {len(chamado.mensagens)} mensagens embutidas.")
