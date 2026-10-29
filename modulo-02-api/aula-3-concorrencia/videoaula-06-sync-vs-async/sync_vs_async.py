"""
VIDEOAULA 6 — Síncrono vs. Assíncrono (tarefas I/O-bound).

Simulamos "atender um chamado" como uma espera de 1 segundo (uma consulta ao banco
ou uma chamada a outro serviço).

Execute:  python sync_vs_async.py
"""

import asyncio
import time

CHAMADOS = ["Sem internet", "Impressora travada", "VPN não conecta"]


# ---------------------------------------------------------------------------
# 1. Versão SÍNCRONA: um por vez, o programa fica parado esperando
# ---------------------------------------------------------------------------
def atender_sync(titulo: str) -> str:
    time.sleep(1)  # espera bloqueante
    return f"Resolvido: {titulo}"


def rodar_sync() -> None:
    inicio = time.perf_counter()
    for titulo in CHAMADOS:
        print(atender_sync(titulo))
    print(f"[sync] total: {time.perf_counter() - inicio:.1f}s\n")


# ---------------------------------------------------------------------------
# 2. Versão ASSÍNCRONA: enquanto um espera, os outros andam
# ---------------------------------------------------------------------------
async def atender_async(titulo: str) -> str:
    await asyncio.sleep(1)  # espera NÃO bloqueante: devolve o controle ao event loop
    return f"Resolvido: {titulo}"


async def rodar_async() -> None:
    inicio = time.perf_counter()
    resultados = await asyncio.gather(*(atender_async(t) for t in CHAMADOS))
    for linha in resultados:
        print(linha)
    print(f"[async] total: {time.perf_counter() - inicio:.1f}s\n")


# ---------------------------------------------------------------------------
# 3. ARMADILHA: usar time.sleep dentro de async def bloqueia TUDO
# ---------------------------------------------------------------------------
async def atender_async_errado(titulo: str) -> str:
    time.sleep(1)  # <- bloqueia o event loop inteiro!
    return f"Resolvido: {titulo}"


async def rodar_async_errado() -> None:
    inicio = time.perf_counter()
    await asyncio.gather(*(atender_async_errado(t) for t in CHAMADOS))
    print(
        f"[async com time.sleep] total: {time.perf_counter() - inicio:.1f}s (sem ganho!)\n"
    )


if __name__ == "__main__":
    print("=== 1. Síncrono ===")
    rodar_sync()
    print("=== 2. Assíncrono ===")
    asyncio.run(rodar_async())
    print("=== 3. Armadilha ===")
    asyncio.run(rodar_async_errado())
