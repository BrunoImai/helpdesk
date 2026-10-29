# Videoaula 9 — O contrato `TicketCreate`: nosso primeiro Schema Pydantic (12 min)

**Objetivo:** criar o modelo que define o que é um chamado válido ao ser aberto.

**Arquivos**
- [`ticket_create.py`](ticket_create.py): schema com `Field` (tamanho mínimo/máximo, padrão, `EmailStr`).
- [`testar_ticket_create.py`](testar_ticket_create.py): casos válido e inválidos para mostrar os erros.

## Como rodar
```powershell
pip install "pydantic[email]"
python testar_ticket_create.py
```

## Roteiro de gravação
1. Escrever `TicketCreate` campo a campo (digitando ao vivo).
2. `Field(min_length=..., max_length=...)` para restringir tamanho.
3. Valores padrão e `Prioridade` como `Enum`.
4. Rodar `testar_ticket_create.py` e ler as mensagens de `ValidationError` (campo, tipo do erro, mensagem).
5. Conectar com o título da aula: "a catraca": dados inválidos nem entram no sistema.
