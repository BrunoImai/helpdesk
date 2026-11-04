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

## O que esperar (testado)
- `ruff check codigo_sujo.py` aponta 8 problemas (E401, I001, F401 x3, E712, E711, N801).
- `ruff check --fix` corrige os automáticos (imports); **sobram 3 de propósito**: E712 (`== True`), E711 (`== None`) e
  N801 (nome da classe). Corrija-os ao vivo (`if urgente:`, `if titulo is None:`, `class Chamado`) para mostrar que
  o linter **avisa** e o formatter **formata**, mas decisões de lógica são suas.
- `black` reformata o arquivo (aspas, espaços, linhas em branco).
- Sem `.env`: `ValidationError ... secret_key Field required`. Com `.env`: a configuração aparece e a chave sai mascarada.
- Para repetir a demonstração: `git checkout -- codigo_sujo.py` (ou `git restore codigo_sujo.py`) devolve o arquivo sujo.

## Roteiro de gravação
1. Abrir `codigo_sujo.py` e rodar `ruff check` (mostrar os códigos F401, E711, E712...).
2. Rodar `ruff check --fix` e depois `black`; comparar o antes e o depois (`git diff`).
3. Explicar por que segredos não ficam no código. Mostrar `.env.example` vs `.env`.
4. Rodar `demo_env.py` e mostrar o erro quando falta uma variável obrigatória (apagar `SECRET_KEY` do `.env`).
5. Reforçar: `.env` está no `.gitignore`.
