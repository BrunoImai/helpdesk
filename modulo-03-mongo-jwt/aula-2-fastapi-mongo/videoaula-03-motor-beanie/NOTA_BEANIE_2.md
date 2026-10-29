# Nota: Motor + Beanie 1.x (usado na trilha) e o Beanie 2.x

O **Motor** foi descontinuado pela MongoDB em favor do driver assíncrono nativo do PyMongo (`AsyncMongoClient`).
As versões **2.x do Beanie** já usam esse novo driver. A trilha ensina **Motor + Beanie 1.x**
(`beanie>=1.30,<2`), que é o que consta nos `requirements.txt`, porque a modelagem, as consultas e todo o
restante do código são idênticos. Só muda a criação do cliente.

## Beanie 1.x (usado nas aulas)
```python
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(settings.mongo_uri)
await init_beanie(database=client[settings.mongo_db_name], document_models=[Ticket])
```

## Beanie 2.x (quem quiser migrar)
```python
from beanie import init_beanie
from pymongo import AsyncMongoClient

client = AsyncMongoClient(settings.mongo_uri)
await init_beanie(database=client[settings.mongo_db_name], document_models=[Ticket])
...
await client.close()   # em AsyncMongoClient, close() é uma corrotina
```
Para migrar basta trocar o `requirements.txt` (`beanie>=2`, sem `motor`) e essas linhas em `database.py`.
Os modelos (`Document`) e as consultas (`find`, `get`, `aggregate`, `set`...) continuam iguais.
