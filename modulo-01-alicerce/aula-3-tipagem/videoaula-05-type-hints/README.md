# Videoaula 5 — O poder dos Type Hints (7 min)

**Objetivo:** anotar funções com tipos e usar o `mypy` para encontrar erros antes de executar.

**Arquivos**
- [`type_hints.py`](type_hints.py): funções sem tipo, com tipo e um erro que só o `mypy` enxerga.

## Como rodar
```powershell
pip install mypy
python type_hints.py        # roda normalmente (Python ignora as anotações)
mypy type_hints.py          # no estado original: "Success" (o erro está escondido por um comentário)
```

> **Atenção:** o erro de propósito (`calcular_sla("oito", ...)`) vem com o comentário `# type: ignore[arg-type]`,
> que silencia o `mypy`. Para a demonstração, **apague esse comentário** no editor e rode `mypy type_hints.py` de
> novo. Esperado (testado):
> ```
> type_hints.py:51: error: Argument 1 to "calcular_sla" has incompatible type "str"; expected "float"  [arg-type]
> ```
> Dependendo da configuração do `mypy`, aparece também `Function is missing a type annotation` (para a função sem
> tipos, `calcular_sla_sem_tipo`): bom gancho para mostrar por que anotar é melhor.

## Roteiro de gravação
1. Mostrar a função sem tipos e a dúvida "o que é `peso`?".
2. Anotar parâmetros e retorno.
3. Rodar o `mypy` e mostrar a mensagem de erro (`Argument 1 ... has incompatible type "str"`).
4. Ponto-chave: type hints não mudam a execução do Python, mas FastAPI e Pydantic as usam em tempo de execução.
