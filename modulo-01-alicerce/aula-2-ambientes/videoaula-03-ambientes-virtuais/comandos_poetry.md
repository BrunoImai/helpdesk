# VIDEOAULA 3 — Alternativa: Poetry

> Rode **um comando por vez** (os comentários `#` ficam em linhas separadas, acima de cada comando).

```powershell
# Instalação (uma vez). Se não tiver o pipx: python -m pip install --user pipx ; python -m pipx ensurepath
# (feche e reabra o terminal depois do ensurepath)
pipx install poetry
poetry --version

# Projeto novo (cria uma pasta com estrutura pronta)
poetry new helpdesk
# OU, dentro de uma pasta existente (responda às perguntas):
poetry init

# Dependências
poetry add fastapi "uvicorn[standard]" "pydantic[email]" pydantic-settings
poetry add --group dev ruff black mypy pytest

# Recria o ambiente a partir do poetry.lock (em outra máquina)
poetry install
# Executa comandos dentro do ambiente, sem ativar
poetry run python mostra_ambiente.py
poetry run uvicorn app.main:app --reload
# Para "entrar" no ambiente (Poetry 2.x): poetry env activate (imprime o comando de ativação)
# No Poetry 1.x: poetry shell
poetry env activate
```

| Tarefa | `venv` + `pip` | Poetry |
|---|---|---|
| Criar ambiente | `python -m venv .venv` | automático |
| Instalar pacote | `pip install x` | `poetry add x` |
| Travar versões | `pip freeze > requirements.txt` | `poetry.lock` (automático) |
| Separar dev/prod | arquivos diferentes | `--group dev` |
| Reproduzir | `pip install -r requirements.txt` | `poetry install` |

Na trilha usaremos `venv` + `pip` por ser nativo do Python; Poetry fica como opção para quem quiser.

> Observação: o Poetry **não foi executado** no ambiente de preparação deste material; teste os comandos antes de gravar.
