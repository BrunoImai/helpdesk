# Avaliação da Aula 1 — Mini Hands-on (gabarito)

**Desafio do aluno:** escrever um **cliente WebSocket em Python** que se conecta ao chat de um chamado, recebe
mensagens em tempo real e envia mensagens digitadas no terminal.

- [`enunciado_aluno.py`](enunciado_aluno.py): ponto de partida com os TODO.
- [`gabarito.py`](gabarito.py): solução esperada (leitura e envio simultâneos, tratamento de recusa).

## Como testar o gabarito
```powershell
pip install websockets
# 1) API rodando (projeto-final) e um chamado criado (POST /tickets); anote o id e o e-mail usado
python gabarito.py <ticket_id> --email cliente@empresa.com
# 2) Em outra janela, abra /chat como suporte (token) ou outro cliente do script e converse
```
Também vale testar a recusa: um `ticket_id` inexistente ou e-mail diferente deve imprimir
"Servidor recusou a conexão" / "Conexão encerrada".

## Critérios de correção
| # | Critério |
|---|---|
| 1 | Usa `websockets.connect` com `async with` (a conexão é fechada corretamente) |
| 2 | Recebe mensagens com `async for` e imprime em tempo real |
| 3 | Envia mensagens com `await ws.send(texto)` |
| 4 | Enviar e receber acontecem **ao mesmo tempo** (duas tarefas, `to_thread(input)`) |
| 5 | A URL leva `ticket_id` e credencial (`?email=` ou `?token=`) |
| 6 | (Bônus) Trata desconexão/recusa sem mostrar traceback |
