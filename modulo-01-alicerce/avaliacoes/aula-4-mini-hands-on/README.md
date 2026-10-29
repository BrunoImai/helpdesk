# Avaliação da Aula 4 — Mini Hands-on (gabarito)

**Desafio do aluno:** escrever o modelo `TicketCreate` e validá-lo passando um dicionário com e-mail incorreto, vendo o erro estourar.

- [`enunciado_aluno.py`](enunciado_aluno.py): arquivo inicial entregue ao aluno (com `TODO`).
- [`gabarito.py`](gabarito.py): solução esperada.

## Como rodar o gabarito
```powershell
pip install "pydantic[email]"
python gabarito.py
```
Saída esperada: uma mensagem informando que o campo `email_solicitante` não é um e-mail válido, e a confirmação de que o dicionário correto é aceito.

## Critérios de correção
| # | Critério |
|---|---|
| 1 | `TicketCreate` herda de `BaseModel` |
| 2 | Campos `titulo` (str), `descricao` (str) e `email_solicitante` (`EmailStr`) |
| 3 | Pelo menos um limite com `Field` (ex.: `min_length`) |
| 4 | O erro de e-mail é capturado com `try/except ValidationError` e a mensagem é exibida |
