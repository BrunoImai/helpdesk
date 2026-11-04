# Videoaula 7 — Tipos restritos: `Enum` e `Literal` (8 min)

**Objetivo:** restringir valores aceitos (status e prioridade do chamado) para evitar "strings soltas".

**Arquivos**
- [`enum_e_literal.py`](enum_e_literal.py): `StatusChamado`, `Prioridade` (Enum) e `Literal`.

## Como rodar
```powershell
python enum_e_literal.py
mypy enum_e_literal.py       # esperado: "Success: no issues found"
```

> Para ver o `mypy` recusar um valor fora do `Literal`, descomente a linha `abrir_por("whatsapp")` e rode de novo.
> Com `mypy --strict`, a comparação `Prioridade.ALTA == "alta"` também é sinalizada (`comparison-overlap`); em
> tempo de execução ela vale `True`, porque `StrEnum` herda de `str`. Não use `--strict` nesta aula.

## Roteiro de gravação
1. O problema: `status = "resolvdo"` (erro de digitação silencioso).
2. `Enum`: agrupa valores nomeados; `StatusChamado.RESOLVIDO.value`.
3. `StrEnum` (Python 3.11+, herda de `str`): serializa bem em JSON/Pydantic e compara com texto (`Prioridade.ALTA == "alta"`).
4. `Literal["baixa", "media", "alta"]`: leve, sem criar classe; o `mypy` valida.
5. Quando usar cada um: `Enum` se o valor tem comportamento/é reutilizado; `Literal` para conjuntos pequenos e locais.
