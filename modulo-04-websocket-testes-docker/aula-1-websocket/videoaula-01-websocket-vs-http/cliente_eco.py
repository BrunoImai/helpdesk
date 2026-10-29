"""
VIDEOAULA 1 — Cliente Python do WebSocket (sem navegador).

Com o servidor rodando (uvicorn servidor_eco:app), execute:
    python cliente_eco.py
Requer: pip install websockets   (já vem junto com `uvicorn[standard]`)
"""

import asyncio

import websockets


async def main() -> None:
    async with websockets.connect("ws://127.0.0.1:8000/ws/eco") as ws:
        print("Servidor:", await ws.recv())  # mensagem de boas-vindas

        for texto in ("olá", "preciso de ajuda com a VPN", "obrigada!"):
            await ws.send(texto)
            print("Enviei  :", texto)
            print("Servidor:", await ws.recv())
            await asyncio.sleep(0.5)


if __name__ == "__main__":
    asyncio.run(main())
