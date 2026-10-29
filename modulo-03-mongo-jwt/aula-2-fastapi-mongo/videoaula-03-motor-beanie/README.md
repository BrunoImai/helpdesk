# Videoaula 3 — Conectando o FastAPI ao banco na nuvem com Motor e Beanie (14 min)

**Objetivo:** configurar a conexão com o MongoDB (Atlas ou local), declarar o primeiro `Document` do Beanie e
inicializar tudo no `lifespan` do FastAPI.

| Peça | Papel |
|---|---|
| **MongoDB** | O banco (guarda documentos) |
| **Motor** | Driver **assíncrono** (conversa com o banco sem bloquear) |
| **Beanie** | ODM: mapeia coleções para classes Pydantic (`Document`) |

**Arquivos**
- [`.env.example`](.env.example), [`config.py`](config.py): `MONGO_URI` e `MONGO_DB_NAME`.
- [`models.py`](models.py): `Ticket(Document)`.
- [`database.py`](database.py): `init_db()` com Motor + `init_beanie`.
- [`main.py`](main.py): `lifespan` e uma rota que conta os chamados.
- [`testar_conexao.py`](testar_conexao.py): `ping` no banco.
- [`conectar_atlas.md`](conectar_atlas.md): passo a passo do Atlas. [`NOTA_BEANIE_2.md`](NOTA_BEANIE_2.md): Beanie 2.x.

## Como rodar
```powershell
pip install -r requirements.txt
copy .env.example .env        # edite com a sua connection string
python testar_conexao.py
uvicorn main:app --reload     # abra /docs e execute GET /total-de-chamados
```

## Roteiro de gravação
1. Criar o cluster e copiar a connection string (`conectar_atlas.md`). **Não mostrar a senha na tela.**
2. Guardar a string no `.env` e ler com `config.py`.
3. Criar `models.py` (`Document`, `Settings.name`).
4. Escrever `init_db()`: `AsyncIOMotorClient` + `init_beanie`.
5. Usar `lifespan` no FastAPI (por que não criar a conexão a cada requisição).
6. Testar com `testar_conexao.py` e depois `GET /total-de-chamados` (retorna `0`).
