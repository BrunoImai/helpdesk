"""
VIDEOAULA 8 (OPCIONAL) — A mesma ideia com um broker de verdade: Redis.

ATENÇÃO: este exemplo NÃO foi executado no ambiente de preparação do curso (não havia Docker/Redis).
Teste antes de gravar. Ele é "didático": para produção, considere ferramentas prontas (ARQ, Celery, RQ).

Preparar:
    docker compose -f docker-compose.redis.yml up -d
    pip install redis
Uso (dois terminais):
    python fila_redis_opcional.py worker       # consumidor
    python fila_redis_opcional.py produtor     # envia 3 tarefas
"""

import asyncio
import json
import sys

import redis.asyncio as redis

FILA = "helpdesk:emails"


async def produtor() -> None:
    r = redis.from_url("redis://localhost:6379", decode_responses=True)
    for i in range(1, 4):
        tarefa = {"titulo": f"#{i}", "email": f"cliente{i}@empresa.com"}
        await r.rpush(FILA, json.dumps(tarefa))  # empurra no fim da lista
        print("enfileirado:", tarefa)
    await r.aclose()


async def worker() -> None:
    r = redis.from_url("redis://localhost:6379", decode_responses=True)
    print("worker aguardando tarefas (Ctrl+C para sair)...")
    while True:
        item = await r.blpop([FILA], timeout=0)  # bloqueia até chegar algo
        if item is None:
            continue
        _, bruto = item
        tarefa = json.loads(bruto)
        await asyncio.sleep(1)  # simula envio de e-mail
        print("e-mail enviado para", tarefa["email"])


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "worker"
    asyncio.run(produtor() if modo == "produtor" else worker())
