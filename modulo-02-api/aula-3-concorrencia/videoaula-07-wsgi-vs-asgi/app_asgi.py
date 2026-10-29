"""
VIDEOAULA 7 — Aplicação ASGI "crua" (assíncrona).

Execute:  uvicorn app_asgi:app --port 8002   e abra http://127.0.0.1:8002/
"""

import asyncio
import json
from collections.abc import Awaitable, Callable, MutableMapping
from typing import Any

Scope = MutableMapping[str, Any]
Receive = Callable[[], Awaitable[MutableMapping[str, Any]]]
Send = Callable[[MutableMapping[str, Any]], Awaitable[None]]


async def app(scope: Scope, receive: Receive, send: Send) -> None:
    """Interface ASGI: `scope` descreve a conexão; `receive`/`send` trocam eventos."""
    if scope["type"] != "http":
        return  # (lifespan e websocket ficam fora do exemplo)

    await asyncio.sleep(0.1)  # aqui podemos usar `await`: algo impossível em WSGI

    corpo = json.dumps({"servidor": "ASGI", "caminho": scope["path"]}).encode("utf-8")
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"application/json")],
        }
    )
    await send({"type": "http.response.body", "body": corpo})
