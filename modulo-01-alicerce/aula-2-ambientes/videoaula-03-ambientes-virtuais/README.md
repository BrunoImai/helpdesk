# Videoaula 3 — Ambientes virtuais: `venv` e Poetry (8 min)

**Objetivo:** isolar as dependências do HelpDesk em um ambiente virtual e saber reproduzi-lo em outra máquina.

**Arquivos**
- [`comandos_venv.md`](comandos_venv.md): fluxo com `venv` + `pip` (padrão da trilha).
- [`comandos_poetry.md`](comandos_poetry.md): o mesmo fluxo com Poetry (alternativa).
- [`requirements.txt`](requirements.txt): dependências do módulo 1.
- [`pyproject.toml`](pyproject.toml): equivalente em Poetry.
- [`mostra_ambiente.py`](mostra_ambiente.py): script que mostra qual Python está sendo usado.

## Roteiro de gravação
1. Problema: "funciona na minha máquina" e conflito de versões entre projetos.
2. Rodar `mostra_ambiente.py` **antes** de ativar o ambiente e **depois** (o caminho do Python muda).
3. Criar, ativar, instalar, congelar (`pip freeze`) e recriar a partir do `requirements.txt`.
4. Apresentar Poetry rapidamente: `pyproject.toml` + `poetry.lock`.
