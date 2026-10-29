# Videoaula 6 — Coleções tipadas e dados opcionais (8 min)

**Objetivo:** tipar `list`, `dict`, `tuple`, `set` e representar valores que podem ser `None` com `X | None`.

**Arquivos**
- [`colecoes_e_opcionais.py`](colecoes_e_opcionais.py)

## Como rodar
```powershell
python colecoes_e_opcionais.py
mypy colecoes_e_opcionais.py
```

## Roteiro de gravação
1. `list[str]`, `dict[str, int]`, `tuple[int, str]`, `set[str]` (sintaxe moderna, sem `typing.List`).
2. O problema do `None`: `buscar_chamado()` pode não encontrar nada.
3. `Optional[X]` é o mesmo que `X | None`. Mostrar o `mypy` reclamando quando não se trata o `None`.
4. Narrowing: `if chamado is None: ...` e o `mypy` entende o resto.
