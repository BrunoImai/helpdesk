"""
VIDEOAULA 6 — Coleções tipadas e dados opcionais.

Execute:  python colecoes_e_opcionais.py
Verifique: mypy colecoes_e_opcionais.py
"""

from typing import Optional  # noqa: UP045  (mostrado só para comparar com `X | None`)

# ---------------------------------------------------------------------------
# 1. Coleções tipadas (Python 3.9+: use list, dict, tuple, set direto)
# ---------------------------------------------------------------------------
tags: list[str] = ["rede", "urgente", "vpn"]
contagem_por_status: dict[str, int] = {"aberto": 5, "em_andamento": 3, "resolvido": 12}
coordenada: tuple[int, str] = (1, "A")  # tupla com posições de tipos diferentes
ids_unicos: set[int] = {1, 2, 3}

# Coleções aninhadas
chamados: list[dict[str, str | int]] = [
    {"id": 1, "titulo": "Sem internet"},
    {"id": 2, "titulo": "Impressora travada"},
]


def titulos(lista: list[dict[str, str | int]]) -> list[str]:
    return [str(item["titulo"]) for item in lista]


# ---------------------------------------------------------------------------
# 2. Dados opcionais: o valor pode não existir
# ---------------------------------------------------------------------------
BANCO: dict[int, str] = {1: "Sem internet", 2: "Impressora travada"}


def buscar_chamado(chamado_id: int) -> str | None:
    """Retorna o título ou None se o chamado não existir."""
    return BANCO.get(chamado_id)


# Forma antiga, equivalente: Optional[str]
def buscar_chamado_antigo(chamado_id: int) -> Optional[str]:  # noqa: UP045
    return BANCO.get(chamado_id)


# ---------------------------------------------------------------------------
# 3. >>> DEMONSTRAÇÃO: tratando o None
# ---------------------------------------------------------------------------
def mostrar_titulo_em_maiusculo(chamado_id: int) -> str:
    titulo = buscar_chamado(chamado_id)

    # Se você escrever `return titulo.upper()` aqui, o mypy acusa:
    #   Item "None" of "str | None" has no attribute "upper"
    if titulo is None:
        return "Chamado não encontrado"
    return titulo.upper()  # aqui o mypy já sabe que `titulo` é str


# Parâmetro opcional com valor padrão
def criar_chamado(titulo: str, descricao: str | None = None) -> dict[str, str | None]:
    return {"titulo": titulo, "descricao": descricao}


if __name__ == "__main__":
    print(titulos(chamados))
    print(mostrar_titulo_em_maiusculo(1))
    print(mostrar_titulo_em_maiusculo(99))
    print(criar_chamado("Sem internet"))
    print(criar_chamado("Sem internet", "Desde as 9h"))
