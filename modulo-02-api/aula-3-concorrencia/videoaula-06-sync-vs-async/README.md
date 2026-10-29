# Videoaula 6 — Síncrono vs. Assíncrono: o gargalo de I/O (10 min)

**Objetivo:** ver, com cronômetro, a diferença entre esperar uma tarefa por vez e aproveitar o tempo de espera.

**Arquivos**
- [`sync_vs_async.py`](sync_vs_async.py): atendimento de 3 chamados de forma síncrona e assíncrona (I/O-bound).
- [`io_vs_cpu.py`](io_vs_cpu.py): por que `async` ajuda no I/O mas **não** em tarefas de CPU.

## Como rodar
```powershell
python sync_vs_async.py
python io_vs_cpu.py
```

## Roteiro de gravação
1. Analogia do atendente: um atendente que fica parado olhando a impressora vs. um que atende outro cliente enquanto espera.
2. Rodar `sync_vs_async.py`: ~3 s (sequencial) vs. ~1 s (concorrente). Mesmo com **uma única thread**.
3. `async def`, `await`, `asyncio.run()` e `asyncio.gather()`.
4. Armadilha: `time.sleep()` dentro de `async def` **bloqueia** o loop (mostrar em `sync_vs_async.py`, bloco 3).
5. `io_vs_cpu.py`: o `async` não acelera cálculo pesado (CPU-bound); para isso, processos/threads.
