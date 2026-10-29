# Videoaula 6 — Isolamento com mocks (15 min)

**Objetivo:** testar sem tocar no banco de produção, em e-mail real ou em serviços externos.

**Arquivos**
- [`test_mock_basico.py`](test_mock_basico.py): auto-contido. `MagicMock`, `AsyncMock`, `patch`, `side_effect`.
- [`projeto/test_tickets_mock.py`](projeto/test_tickets_mock.py): o caso real do HelpDesk (cópia de
  `projeto-final/tests/api/`), com `dependency_overrides` + serviço falso.

## Como rodar
```powershell
pip install pytest pytest-asyncio
pytest test_mock_basico.py -v           # exemplo auto-contido
# No projeto final:
cd ..\..\projeto-final
pytest tests/api/test_tickets_mock.py -v
```

## Três ferramentas, três usos
| Ferramenta | Quando usar |
|---|---|
| `MagicMock` / `AsyncMock` | Objeto falso: define retorno (`return_value`) e verifica chamadas (`assert_called...`) |
| `patch("modulo.nome")` | Trocar uma função **onde ela é usada** (e-mail, relógio, API externa) |
| `app.dependency_overrides` | Específico do FastAPI: troca uma **dependência** (service, usuário logado) no teste |

> **Cuidado:** mock demais testa o mock, não o sistema. Use para isolar o que é lento ou perigoso; mantenha
> também testes de integração (com o banco falso) como em `test_tickets_db.py`.

## Roteiro de gravação
1. Problema: o teste de abrir chamado demora 2 s e "envia e-mail de verdade" (mostrar o teste lento *skipado*).
2. `MagicMock` e `return_value`; `assert_called_once_with`.
3. `patch` + `AsyncMock` (e a regra "patch onde é usado").
4. `side_effect` para simular falhas.
5. No projeto: `ServicoFalso` + `dependency_overrides` (e **limpar no fim**: `dependency_overrides.clear()`).
6. Fixture autouse do `conftest.py` que bloqueia e-mails em **todos** os testes.
