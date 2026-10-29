"""
MÓDULO 00 — TESTE DE PROFICIÊNCIA (DIAGNÓSTICO)

Banco de trechos de código para montar as questões do teste diagnóstico.
Cada bloco tem: enunciado, trecho, alternativas e gabarito.
Pré-requisitos avaliados: funções, listas/dicionários, classes, exceções e leitura de código.

Rode este arquivo para conferir que todos os gabaritos estão corretos:
    python modulo-00-diagnostico/exercicios_diagnostico.py
"""

# ---------------------------------------------------------------------------
# Questão 1 — Funções e valores padrão
# O que será impresso?
# A) 5   B) 7   C) 10   D) Erro
# Gabarito: B
# ---------------------------------------------------------------------------
def somar(a, b=2):
    return a + b


# ---------------------------------------------------------------------------
# Questão 2 — Listas e compreensão de listas
# O que `pares` contém?
# A) [2, 4]   B) [1, 3, 5]   C) [2, 4, 6]   D) [1, 2, 3, 4, 5]
# Gabarito: A
# ---------------------------------------------------------------------------
numeros = [1, 2, 3, 4, 5]
pares = [n for n in numeros if n % 2 == 0]


# ---------------------------------------------------------------------------
# Questão 3 — Dicionários
# O que `chamado.get("prioridade", "baixa")` retorna?
# A) None   B) KeyError   C) "baixa"   D) "alta"
# Gabarito: C
# ---------------------------------------------------------------------------
chamado = {"id": 1, "titulo": "Sem internet"}


# ---------------------------------------------------------------------------
# Questão 4 — Classes
# O que é impresso por `print(Atendente("Ana").saudacao())`?
# A) "Olá, Ana"   B) "Olá, nome"   C) Erro   D) None
# Gabarito: A
# ---------------------------------------------------------------------------
class Atendente:
    def __init__(self, nome):
        self.nome = nome

    def saudacao(self):
        return f"Olá, {self.nome}"


# ---------------------------------------------------------------------------
# Questão 5 — Exceções
# Qual é a saída?
# A) "ok"   B) "erro"   C) "erro" e depois "fim"   D) "fim"
# Gabarito: C
# ---------------------------------------------------------------------------
def questao_excecao() -> list[str]:
    saida: list[str] = []
    try:
        int("abc")
        saida.append("ok")
    except ValueError:
        saida.append("erro")
    finally:
        saida.append("fim")
    return saida


# ---------------------------------------------------------------------------
# Questão 6 — Módulos e pacotes
# Qual comando instala o pacote `fastapi`?
# A) python install fastapi   B) pip install fastapi
# C) pip get fastapi          D) import fastapi
# Gabarito: B
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    assert somar(5) == 7
    assert pares == [2, 4]
    assert chamado.get("prioridade", "baixa") == "baixa"
    assert Atendente("Ana").saudacao() == "Olá, Ana"
    assert questao_excecao() == ["erro", "fim"]
    print("Todos os gabaritos do diagnóstico conferem.")
