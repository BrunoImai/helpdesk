# Videoaula 7 — Tipos restritos: `Enum` e `Literal` (8 min)

**Objetivo:** restringir valores aceitos (status e prioridade do chamado) para evitar "strings soltas".

**Arquivos**
- [`enum_e_literal.py`](enum_e_literal.py): `StatusChamado`, `Prioridade` (Enum) e `Literal`.

## Como rodar
```powershell
python enum_e_literal.py
mypy enum_e_literal.py
```

## Roteiro de gravação
1. O problema: `status = "resolvdo"` (erro de digitação silencioso).
2. `Enum`: agrupa valores nomeados; `StatusChamado.RESOLVIDO.value`.
3. `StrEnum` (Python 3.11+, herda de `str`): serializa bem em JSON/Pydantic e compara com texto (`Prioridade.ALTA == "alta"`).
4. `Literal["baixa", "media", "alta"]`: leve, sem criar classe; o `mypy` valida.
5. Quando usar cada um: `Enum` se o valor tem comportamento/é reutilizado; `Literal` para conjuntos pequenos e locais.
