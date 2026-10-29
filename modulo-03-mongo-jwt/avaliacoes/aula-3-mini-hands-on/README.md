# Avaliação da Aula 3 — Mini Hands-on (gabarito)

**Desafio do aluno:** escrever a query do banco de dados (Beanie) para uma nova rota que liste **exclusivamente**
os chamados com status "resolvido".

- [`enunciado_aluno.py`](enunciado_aluno.py): ponto de partida.
- [`gabarito.py`](gabarito.py): solução esperada. Demais arquivos: base da Videoaula 3.

## Como rodar o gabarito
```powershell
pip install -r requirements.txt
copy .env.example .env      # com a sua connection string
uvicorn gabarito:app --reload
```
Crie chamados (use `POST /tickets` do projeto da Videoaula 4 ou insira direto no Atlas) com status variados e verifique se
`GET /tickets/resolvidos` devolve apenas os `resolvido`.

## Critérios de correção
| # | Critério |
|---|---|
| 1 | A rota é `async def` e usa `await` na consulta |
| 2 | A consulta usa `Ticket.find(Ticket.status == StatusChamado.RESOLVIDO)` (ou `{"status": "resolvido"}`) |
| 3 | Usa `.to_list()` para materializar o resultado |
| 4 | Devolve `list[TicketOut]` |
| 5 | Chamados com outro status (aberto, cancelado...) **não** aparecem na resposta |
