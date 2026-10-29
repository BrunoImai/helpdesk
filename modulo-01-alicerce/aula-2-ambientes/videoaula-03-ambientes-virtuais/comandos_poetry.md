# VIDEOAULA 3 — Alternativa: Poetry

```bash
# Instalação (uma vez)
pipx install poetry
poetry --version

# Novo projeto ou projeto existente
poetry new helpdesk          # cria estrutura nova
# ou, dentro de uma pasta existente:
poetry init

# Dependências
poetry add fastapi "uvicorn[standard]" "pydantic[email]" pydantic-settings
poetry add --group dev ruff black mypy pytest

# Executando
poetry install               # recria o ambiente a partir do poetry.lock
poetry run python mostra_ambiente.py
poetry run uvicorn app.main:app --reload
poetry shell                 # entra no ambiente (ou use `poetry env activate`)
```

| Tarefa | `venv` + `pip` | Poetry |
|---|---|---|
| Criar ambiente | `python -m venv .venv` | automático |
| Instalar pacote | `pip install x` | `poetry add x` |
| Travar versões | `pip freeze > requirements.txt` | `poetry.lock` (automático) |
| Separar dev/prod | arquivos diferentes | `--group dev` |
| Reproduzir | `pip install -r requirements.txt` | `poetry install` |

Na trilha usaremos `venv` + `pip` por ser nativo do Python; Poetry fica como opção para quem quiser.
