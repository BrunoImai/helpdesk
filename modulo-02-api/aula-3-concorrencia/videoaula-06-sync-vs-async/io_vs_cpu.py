"""
VIDEOAULA 6 — I/O-bound vs. CPU-bound.

- I/O-bound: o tempo é gasto ESPERANDO (rede, disco, banco). async ajuda muito.
- CPU-bound: o tempo é gasto CALCULANDO. async NÃO ajuda (continua em uma thread).

Execute:  python io_vs_cpu.py
"""

import asyncio
import time


def calculo_pesado(n: int = 3_000_000) -> int:
    """Tarefa de CPU: soma de quadrados."""
    return sum(i * i for i in range(n))


async def tarefa_cpu_async(n: int) -> int:
    return calculo_pesado(n)  # não há `await` real: nada é devolvido ao loop


async def tarefa_io_async() -> None:
    await asyncio.sleep(0.5)


async def main() -> None:
    # --- CPU-bound com async: sem ganho --------------------------------------
    inicio = time.perf_counter()
    await asyncio.gather(*(tarefa_cpu_async(3_000_000) for _ in range(3)))
    print(
        f"3 tarefas CPU com async : {time.perf_counter() - inicio:.2f}s (soma dos tempos)"
    )

    # --- I/O-bound com async: ganho enorme -----------------------------------
    inicio = time.perf_counter()
    await asyncio.gather(*(tarefa_io_async() for _ in range(3)))
    print(
        f"3 tarefas I/O com async : {time.perf_counter() - inicio:.2f}s (tempo de UMA)"
    )

    # --- Solução para CPU-bound dentro de código async: thread/processo ------
    inicio = time.perf_counter()
    await asyncio.gather(*(asyncio.to_thread(calculo_pesado) for _ in range(3)))
    print(
        f"3 tarefas CPU com threads: {time.perf_counter() - inicio:.2f}s "
        "(a GIL limita; para ganho real use multiprocessing)"
    )


if __name__ == "__main__":
    asyncio.run(main())
