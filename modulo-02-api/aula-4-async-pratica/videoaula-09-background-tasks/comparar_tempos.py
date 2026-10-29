"""
VIDEOAULA 9 — Compara o tempo de resposta COM e SEM BackgroundTasks.

Sobe um servidor Uvicorn de verdade em segundo plano (porta 8765) e mede o tempo
que o CLIENTE espera pela resposta.

Execute:  python comparar_tempos.py
"""

import threading
import time

import httpx
import uvicorn
from main import app

PORTA = 8765
URL = f"http://127.0.0.1:{PORTA}"
DADOS = {"titulo": "Sem acesso à VPN", "email_solicitante": "ana@empresa.com"}


def subir_servidor() -> uvicorn.Server:
    config = uvicorn.Config(app, host="127.0.0.1", port=PORTA, log_level="warning")
    servidor = uvicorn.Server(config)
    threading.Thread(target=servidor.run, daemon=True).start()
    while not servidor.started:
        time.sleep(0.05)
    return servidor


def tempo_de_resposta(rota: str) -> float:
    inicio = time.perf_counter()
    resposta = httpx.post(f"{URL}{rota}", json=DADOS, timeout=10)
    resposta.raise_for_status()
    return time.perf_counter() - inicio


if __name__ == "__main__":
    servidor = subir_servidor()
    try:
        sem = tempo_de_resposta("/tickets-lento")
        com = tempo_de_resposta("/tickets")
        print(f"SEM BackgroundTasks: cliente esperou {sem:.2f}s")
        print(f"COM BackgroundTasks: cliente esperou {com:.2f}s")
        time.sleep(2.2)  # dá tempo da tarefa de fundo terminar e aparecer no log
    finally:
        servidor.should_exit = True
