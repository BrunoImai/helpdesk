# Videoaula 4 — Linters, Formatters e variáveis de ambiente (12 min)

**Objetivo:** padronizar o código com `ruff` e `black`, e guardar configurações sensíveis em `.env`.

**Arquivos**
- [`codigo_sujo.py`](codigo_sujo.py): código propositalmente mal escrito para o linter e o formatter corrigirem.
- [`pyproject.toml`](pyproject.toml): configuração do `ruff`, `black` e `mypy`.
- [`.env.example`](.env.example): modelo versionado (sem segredos reais).
- [`config.py`](config.py): leitura tipada do `.env` com `pydantic-settings`.
- [`demo_env.py`](demo_env.py): mostra a configuração carregada (a chave é mascarada).

## Como rodar (dentro desta pasta, com o ambiente ativo)
```powershell
pip install ruff black pydantic-settings
ruff check codigo_sujo.py          # lista os problemas
ruff check codigo_sujo.py --fix    # corrige o que for automático
black codigo_sujo.py               # formata
copy .env.example .env             # crie o seu .env (NUNCA vai para o Git)
python demo_env.py
```

## Roteiro de gravação
1. Abrir `codigo_sujo.py` e rodar `ruff check` (mostrar os códigos F401, E711, E712...).
2. Rodar `ruff check --fix` e depois `black`; comparar o antes e o depois (`git diff`).
3. Explicar por que segredos não ficam no código. Mostrar `.env.example` vs `.env`.
4. Rodar `demo_env.py` e mostrar o erro quando falta uma variável obrigatória (apagar `SECRET_KEY` do `.env`).
5. Reforçar: `.env` está no `.gitignore`.
