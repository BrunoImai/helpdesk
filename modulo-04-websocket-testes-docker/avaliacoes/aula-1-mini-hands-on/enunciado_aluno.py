"""
MINI HANDS-ON — Aula 1 (WebSocket): cliente de terminal para o chat do HelpDesk.

Complete os TODO. Requer: pip install websockets
Uso: python enunciado_aluno.py <ticket_id> <email_do_chamado>
"""

import asyncio
import sys


async def main(ticket_id: str, email: str) -> None:
    url = f"ws://127.0.0.1:8000/ws/tickets/{ticket_id}?email={email}"

    # TODO 1: conecte com `websockets.connect(url)` (use `async with`).
    # TODO 2: receba mensagens em um laço `async for` e imprima cada uma.
    # TODO 3: envie ao menos uma mensagem de texto com `await ws.send(...)`.
    # DESAFIO: leia o teclado SEM travar o recebimento (dica: asyncio.to_thread(input)).
    raise NotImplementedError


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2]))
