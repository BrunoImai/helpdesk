# HelpDesk — Projeto final do Módulo 1

Estado do projeto ao final do Módulo 1: repositório organizado, ambiente virtual, configurações em `.env`
e as primeiras "catracas" (Schemas Pydantic).

```
projeto-final/
  app/
    core/config.py          # Settings lidas do .env (pydantic-settings)
    schemas/enums.py        # StatusChamado e Prioridade
    schemas/ticket.py       # TicketCreate com validadores
  scripts/validar_ticket.py # demonstração das catracas
  .env.example  .gitignore  requirements.txt  pyproject.toml
```

## Desafio hands-on do Módulo 1 (checklist)
1. Criar o repositório `helpdesk` no GitHub e conectá-lo (`git remote add origin ...`).
2. Criar e ativar o ambiente virtual; instalar `requirements.txt`.
3. Copiar `.env.example` para `.env`.
4. Rodar `python -m scripts.validar_ticket` e ver aceitos e rejeitados.
5. Fazer commits pequenos em uma branch `feature/ticket-create` e abrir um Pull Request.

## Como rodar
```powershell
cd modulo-01-alicerce\projeto-final
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python -m scripts.validar_ticket
ruff check . ; black --check .
```
