# Videoaula 12 — Configurando o Pytest e o TestClient (12 min)

**Objetivo:** escrever e rodar os primeiros testes de API.

| Arquivo | Papel |
|---|---|
| [`app_exemplo.py`](app_exemplo.py) | Mini API (sem banco) para testar |
| [`conftest.py`](conftest.py) | Fixtures `client` e `chamado_criado` |
| [`test_app_exemplo.py`](test_app_exemplo.py) | Os testes |
| [`pytest.ini`](pytest.ini) | Configuração |

## Como rodar
```powershell
pip install pytest httpx fastapi
pytest
pytest -k criar          # só testes com "criar" no nome
pytest -x                # para no primeiro erro
```
Esperado: `6 passed`.

## Conceitos
- Descoberta automática: arquivos `test_*.py`, funções `test_*`.
- `assert` simples; o Pytest mostra o diff quando falha.
- **Fixtures** (`conftest.py`): preparam o que o teste precisa (e limpam depois, com `yield`).
- `@pytest.mark.parametrize`: o mesmo teste com várias entradas.
- `TestClient`: chama a API **sem subir servidor** (`client.get/post(...)`).
- Padrão **Arrange -> Act -> Assert**.

## Roteiro de gravação
1. Instalar e rodar `pytest` com o primeiro teste (`test_raiz_responde_ok`).
2. Mostrar uma falha proposital (renomeie `x_test_falha_de_proposito` para `test_falha_de_proposito`) e como ler a mensagem de erro.
3. Fixtures e `conftest.py`; isolamento entre testes.
4. `parametrize` com títulos inválidos (422).
5. Fechamento: no `projeto-final` do HelpDesk, a mesma ideia está em `tests/test_main.py`.
