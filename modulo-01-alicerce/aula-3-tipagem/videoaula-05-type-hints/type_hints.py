"""
VIDEOAULA 5 — O poder dos Type Hints.

Execute:  python type_hints.py
Verifique: mypy type_hints.py
"""


# ---------------------------------------------------------------------------
# 1. Sem tipos: o que essa função espera receber?
# ---------------------------------------------------------------------------
def calcular_sla_sem_tipo(horas, urgente):
    if urgente:
        return horas / 2
    return horas


# ---------------------------------------------------------------------------
# 2. Com tipos: a função "se documenta"
# ---------------------------------------------------------------------------
def calcular_sla(horas: float, urgente: bool) -> float:
    """Retorna o prazo de atendimento em horas (urgentes têm metade do prazo)."""
    if urgente:
        return horas / 2
    return horas


# ---------------------------------------------------------------------------
# 3. Variáveis e retorno vazio
# ---------------------------------------------------------------------------
titulo: str = "Impressora não funciona"
total_chamados: int = 12
resolvido: bool = False


def registrar_log(mensagem: str) -> None:
    print(f"[LOG] {mensagem}")


# ---------------------------------------------------------------------------
# 4. >>> DEMONSTRAÇÃO: o erro que o mypy pega antes da execução
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print(calcular_sla(8, urgente=True))
    registrar_log(titulo)

    # O mypy acusa: Argument 1 to "calcular_sla" has incompatible type "str"
    # Em tempo de execução, o erro só apareceria dentro da função (TypeError),
    # e apenas no caminho `urgente=True`: um bug que "dorme" até alguém passar por ali.
    # Remova o comentário `# type: ignore` ao vivo para mostrar o erro no mypy.
    prazo = calcular_sla("oito", urgente=False)  # type: ignore[arg-type]
    print(prazo)
