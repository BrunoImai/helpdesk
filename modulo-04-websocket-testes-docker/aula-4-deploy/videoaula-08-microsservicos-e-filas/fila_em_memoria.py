"""
VIDEOAULA 8 — Fila de mensagens: o conceito, em memória (sem instalar nada).

Cenário HelpDesk: a API recebe um chamado e DEVOLVE a resposta na hora; o envio de e-mail
vira uma "tarefa" na fila e um worker (consumidor) cuida dela em paralelo.

   API (produtor) --> [ FILA ] --> worker (consumidor)

Execute:  python fila_em_memoria.py
Limite: a fila vive na memória deste processo. Em produção, use um broker
(Redis, RabbitMQ...) para que API e workers sejam processos/containers diferentes.
"""

import asyncio
import time


async def worker(nome: str, fila: asyncio.Queue[dict[str, str] | None]) -> None:
    """Consumidor: pega tarefas da fila até receber o sinal de parada (None)."""
    while True:
        tarefa = await fila.get()
        if tarefa is None:
            fila.task_done()
            return
        await asyncio.sleep(1)  # simula o envio de e-mail (lento)
        print(
            f"  [{nome}] e-mail enviado para {tarefa['email']} (chamado {tarefa['titulo']!r})"
        )
        fila.task_done()


async def api_abrir_chamado(
    fila: asyncio.Queue[dict[str, str] | None], titulo: str, email: str
) -> str:
    """Produtor: grava o chamado e só ENFILEIRA o e-mail — resposta imediata."""
    await fila.put({"titulo": titulo, "email": email})
    return f"chamado {titulo!r} aberto"


async def main() -> None:
    fila: asyncio.Queue[dict[str, str] | None] = asyncio.Queue()
    workers = [asyncio.create_task(worker(f"worker-{i}", fila)) for i in (1, 2)]

    inicio = time.perf_counter()
    for i in range(1, 7):
        resposta = await api_abrir_chamado(fila, f"#{i}", f"cliente{i}@empresa.com")
        print(f"API respondeu em {time.perf_counter() - inicio:.2f}s: {resposta}")

    print("... a API já respondeu a todos; os workers ainda trabalham ...")
    await fila.join()  # espera esvaziar
    for _ in workers:
        await fila.put(None)  # sinal de parada, um por worker
    await asyncio.gather(*workers)
    print(
        f"Tudo processado em {time.perf_counter() - inicio:.2f}s (6 e-mails de 1 s com 2 workers ~ 3 s)"
    )


if __name__ == "__main__":
    asyncio.run(main())
