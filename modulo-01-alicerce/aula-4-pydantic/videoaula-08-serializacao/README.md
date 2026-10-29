# Videoaula 8 — O que é serialização? JSON <-> Python (8 min)

**Objetivo:** entender como objetos Python viram texto JSON (e voltam), e por que o Pydantic faz isso melhor que o módulo `json` puro.

**Arquivos**
- [`serializacao.py`](serializacao.py)

## Como rodar
```powershell
pip install "pydantic[email]"
python serializacao.py
```

## Roteiro de gravação
1. Analogia: enviar um objeto pelo correio = desmontar (serializar) e montar de novo (desserializar).
2. `json.dumps` / `json.loads` e suas limitações (`datetime`, `Enum` não serializam sozinhos).
3. Pydantic: `model_dump()`, `model_dump_json()`, `model_validate()`, `model_validate_json()`.
4. Mostrar que o JSON de entrada é **validado** e convertido (`"10"` vira `10`).
