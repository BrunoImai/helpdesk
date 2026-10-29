# Videoaula 9 — Tarefas de fundo (`BackgroundTasks`): enviando e-mail sem travar a resposta (14 min)

**Objetivo:** responder ao cliente imediatamente e executar a tarefa demorada (e-mail) depois.

**Arquivos**
- [`main.py`](main.py): rota que abre chamado, com versão **sem** e **com** `BackgroundTasks`.
- [`comparar_tempos.py`](comparar_tempos.py): mede o tempo de resposta das duas versões.

## Como rodar
```powershell
pip install fastapi "uvicorn[standard]" httpx "pydantic[email]"
python comparar_tempos.py
uvicorn main:app --reload
```
Observe no terminal do `uvicorn` as mensagens de log "Enviando e-mail..." aparecendo **depois** da resposta.

## Roteiro de gravação
1. Problema: enviar e-mail leva 2 s e o usuário fica esperando a tela.
2. Rota `/tickets-lento`: o `await enviar_email(...)` atrasa a resposta.
3. Rota `/tickets`: `background_tasks.add_task(enviar_email, ...)`. A resposta sai na hora.
4. Limitações: se o servidor cair, a tarefa se perde. Para algo crítico, usar filas (Módulo 4, Redis/RabbitMQ/Celery).
5. Funciona com função `def` ou `async def`.
