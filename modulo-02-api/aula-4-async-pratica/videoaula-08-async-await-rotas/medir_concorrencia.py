"""
VIDEOAULA 8 — Mede quanto tempo 5 requisições simultâneas levam em cada rota.

Execute:  python medir_concorrencia.py
(Não precisa subir o servidor: usa o transporte ASGI do httpx.)
"""

import asyncio
import time

import httpx
from main import app

REQUISICOES = 5


async def medir(rota: str) -> float:
    transporte = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transporte, base_url="http://helpdesk"
    ) as cliente:
        inicio = time.perf_counter()
        await asyncio.gather(*(cliente.get(rota) for _ in range(REQUISICOES)))
        return time.perf_counter() - inicio


async def main() -> None:
    print(f"{REQUISICOES} requisições simultâneas em cada rota:\n")
    for rota in ("/async", "/sync", "/async-bloqueante"):
        tempo = await medir(rota)
        print(f"  {rota:<20} {tempo:.1f}s")


if __name__ == "__main__":
    asyncio.run(main())
