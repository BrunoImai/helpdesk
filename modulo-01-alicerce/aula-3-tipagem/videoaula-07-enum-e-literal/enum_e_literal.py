"""
VIDEOAULA 7 — Tipos restritos: Enum e Literal.

Execute:  python enum_e_literal.py
Verifique: mypy enum_e_literal.py
"""

from enum import StrEnum
from typing import Literal


# ---------------------------------------------------------------------------
# 1. O problema: strings soltas
# ---------------------------------------------------------------------------
def fechar_chamado_fragil(status: str) -> str:
    if status == "resolvido":  # e se alguém digitar "resolvdo"? Nada avisa.
        return "Chamado encerrado"
    return "Continua aberto"


# ---------------------------------------------------------------------------
# 2. Enum: valores nomeados e fechados
# ---------------------------------------------------------------------------
class StatusChamado(StrEnum):
    ABERTO = "aberto"
    EM_ANDAMENTO = "em_andamento"
    RESOLVIDO = "resolvido"
    CANCELADO = "cancelado"


class Prioridade(StrEnum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"


def fechar_chamado(status: StatusChamado) -> str:
    if status == StatusChamado.RESOLVIDO:
        return "Chamado encerrado"
    return "Continua aberto"


# ---------------------------------------------------------------------------
# 3. Literal: conjunto pequeno de valores, sem criar classe
# ---------------------------------------------------------------------------
Canal = Literal["email", "telefone", "chat"]


def abrir_por(canal: Canal) -> str:
    return f"Chamado aberto via {canal}"


# ---------------------------------------------------------------------------
# 4. >>> DEMONSTRAÇÃO
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print(fechar_chamado_fragil("resolvdo"))  # erro de digitação passa batido
    print(fechar_chamado(StatusChamado.RESOLVIDO))

    print(StatusChamado.RESOLVIDO.value)  # "resolvido"
    print(StatusChamado("em_andamento"))  # busca o membro pelo valor
    print([s.value for s in StatusChamado])  # iterando os membros
    print(Prioridade.ALTA == "alta")  # True, porque herda de str

    print(abrir_por("chat"))
    # abrir_por("whatsapp")  # <- descomente: o mypy acusa o valor fora do Literal

    try:
        StatusChamado("resolvdo")
    except ValueError as erro:
        print(f"Enum rejeita valor inválido em tempo de execução: {erro}")
