# Videoaula 10 — Validadores customizados: rejeitando e-mails inválidos na porta (15 min)

**Objetivo:** ir além das validações prontas e criar regras de negócio com `@field_validator` e `@model_validator`.

**Arquivos**
- [`ticket_create.py`](ticket_create.py): `TicketCreate` com validadores (e-mail corporativo, título normalizado, tags limpas, regra de prioridade).
- [`testar_validadores.py`](testar_validadores.py): casos de sucesso e de rejeição.

## Como rodar
```powershell
pip install "pydantic[email]"
python testar_validadores.py
```

## Roteiro de gravação
1. Problema: `EmailStr` aceita `joao@mailinator.com` (e-mail descartável). Nossa regra é bloquear isso.
2. `@field_validator("email_solicitante")`: normalizar (minúsculas) e rejeitar domínios proibidos.
3. `mode="before"` vs. `mode="after"` (limpar o texto antes ou checar depois do tipo).
4. `@model_validator(mode="after")`: regra entre campos (prioridade ALTA exige descrição detalhada).
5. Mostrar como o erro vira resposta 422 no FastAPI (será visto no Módulo 2).
