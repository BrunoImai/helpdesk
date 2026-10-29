"""
GABARITO — Mini hands-on da Aula 1 (WebSocket): cliente de terminal para o chat do HelpDesk.

Uso (com a API rodando em http://127.0.0.1:8000):
    python gabarito.py <ticket_id> --email cliente@empresa.com
    python gabarito.py <ticket_id> --token <JWT>
Digite uma mensagem e tecle Enter para enviar. Ctrl+C (ou linha vazia + Ctrl+Z/Ctrl+D) para sair.
Requer: pip install websockets
"""

import argparse
import asyncio
import json
from urllib.parse import urlencode

import websockets


def formatar(evento: dict) -> str:
    """Transforma o JSON recebido do servidor em uma linha legível."""
    tipo = evento.get("tipo")
    if tipo == "historico":
        linhas = [f"  {m['autor']}: {m['texto']}" for m in evento["mensagens"]]
        return (
            "--- histórico ---\n"
            + ("\n".join(linhas) or "  (vazio)")
            + "\n-----------------"
        )
    if tipo == "mensagem":
        return f"{evento['autor']}: {evento['texto']}"
    if tipo == "sistema":
        return f"* {evento['texto']}"
    return str(evento)


async def receber(ws: websockets.ClientConnection) -> None:
    async for bruto in ws:  # termina sozinho quando a conexão fecha
        print(formatar(json.loads(bruto)))


async def enviar(ws: websockets.ClientConnection) -> None:
    while True:
        # input() bloqueia; to_thread evita travar o recebimento de mensagens
        texto = await asyncio.to_thread(input)
        if texto.strip():
            await ws.send(texto)


async def main(url: str) -> None:
    try:
        async with websockets.connect(url) as ws:
            print("Conectado! Digite e tecle Enter.")
            tarefas = [
                asyncio.create_task(receber(ws)),
                asyncio.create_task(enviar(ws)),
            ]
            _, pendentes = await asyncio.wait(
                tarefas, return_when=asyncio.FIRST_COMPLETED
            )
            for tarefa in pendentes:
                tarefa.cancel()
    except websockets.exceptions.InvalidStatus as erro:
        print(f"Servidor recusou a conexão: HTTP {erro.response.status_code}")
    except websockets.exceptions.ConnectionClosed as erro:
        print(
            f"Conexão encerrada pelo servidor (código {erro.rcvd.code if erro.rcvd else '?'})"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cliente de chat do HelpDesk")
    parser.add_argument("ticket_id")
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--email", help="e-mail do solicitante (cliente)")
    grupo.add_argument("--token", help="JWT do atendente (suporte)")
    parser.add_argument("--host", default="127.0.0.1:8000")
    args = parser.parse_args()

    credencial = {"email": args.email} if args.email else {"token": args.token}
    asyncio.run(
        main(f"ws://{args.host}/ws/tickets/{args.ticket_id}?{urlencode(credencial)}")
    )
