# Videoaula 5 — O poder dos Type Hints (7 min)

**Objetivo:** anotar funções com tipos e usar o `mypy` para encontrar erros antes de executar.

**Arquivos**
- [`type_hints.py`](type_hints.py): funções sem tipo, com tipo e um erro que só o `mypy` enxerga.

## Como rodar
```powershell
pip install mypy
python type_hints.py        # roda normalmente (Python ignora as anotações)
mypy type_hints.py          # o mypy aponta o erro de tipo
```

## Roteiro de gravação
1. Mostrar a função sem tipos e a dúvida "o que é `peso`?".
2. Anotar parâmetros e retorno.
3. Rodar o `mypy` e mostrar a mensagem de erro (`Argument 1 ... has incompatible type "str"`).
4. Ponto-chave: type hints não mudam a execução do Python, mas FastAPI e Pydantic as usam em tempo de execução.
