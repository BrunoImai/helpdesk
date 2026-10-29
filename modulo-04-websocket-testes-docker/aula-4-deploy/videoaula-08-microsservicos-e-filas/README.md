# Videoaula 8 — Microsserviços e filas de mensagens (10 min, conceitual)

**Objetivo:** entender, sem implementar, como o HelpDesk poderia crescer: serviços separados que conversam
por filas.

## Monólito x microsserviços
```mermaid
flowchart LR
    subgraph Monolito["Hoje: monólito (1 app FastAPI)"]
        A[Chamados + Auth + Chat + E-mail]
    end
    subgraph Micro["Amanhã: serviços separados"]
        T[Serviço de Chamados]
        U[Serviço de Autenticação]
        C[Serviço de Chat]
        N[Serviço de Notificações]
    end
    T -- evento "chamado.criado" --> F[(Fila / Broker)]
    F --> N
    F --> C
```

| | Monólito | Microsserviços |
|---|---|---|
| Deploy | Um só | Vários, independentes |
| Escala | Tudo junto | Só o que precisa (ex.: chat) |
| Complexidade | Baixa | Alta (rede, observabilidade, versões) |
| Quando usar | Começo / times pequenos | Times grandes, partes com cargas muito diferentes |

## Por que filas?
- **Desacoplam**: quem produz não espera quem consome (a API responde em ms; o e-mail sai depois).
- **Absorvem picos**: a fila "segura" o excesso.
- **Resiliência**: se o worker cair, as tarefas esperam na fila.
- Brokers comuns: Redis, RabbitMQ, Kafka, SQS.
- Ligação com o curso: o `BackgroundTasks` do Módulo 2 faz isto *dentro do processo*; a fila faz entre processos.
- Ligação com o chat: o `ConnectionManager` em memória não funciona com vários workers; **Redis Pub/Sub** distribui
  as mensagens entre eles.

## Demonstração
```powershell
python fila_em_memoria.py
```
Mostre que a API responde em ~0 s enquanto os workers enviam os e-mails (6 tarefas de 1 s, 2 workers = ~3 s).

**Opcional (não validado aqui — teste antes de gravar):** [`fila_redis_opcional.py`](fila_redis_opcional.py) com
[`docker-compose.redis.yml`](docker-compose.redis.yml).

## Roteiro de gravação
1. Dor: "o e-mail demora 2 s e a API fica esperando".
2. Desenho monólito -> serviços; custo da complexidade (não existe "melhor", existe adequado).
3. Produtor / fila / consumidor com `fila_em_memoria.py`.
4. Mencionar o broker real e o Pub/Sub do chat. Sem implementação obrigatória.
