"""
VIDEOAULA 1 — Protocolo WebSocket vs. requisições HTTP.

Um servidor com as duas formas de comunicação lado a lado:
  - HTTP : o cliente PERGUNTA, o servidor responde, a conexão acaba.
  - WS   : a conexão fica ABERTA e os dois lados falam quando quiserem.

Execute:  uvicorn servidor_eco:app --reload
Abra:     http://127.0.0.1:8000/        (página de teste)
          http://127.0.0.1:8000/docs    (repare: o Swagger NÃO lista WebSockets)
"""

from datetime import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI(title="HelpDesk — WebSocket vs HTTP")


# ---------------------------------------------------------------------------
# 1. HTTP: cada pergunta abre uma requisição nova (e o servidor não pode "avisar" ninguém)
# ---------------------------------------------------------------------------
@app.get("/hora")
async def hora_http() -> dict[str, str]:
    return {"hora": datetime.now().strftime("%H:%M:%S")}


# ---------------------------------------------------------------------------
# 2. WebSocket: uma conexão, várias mensagens, nos dois sentidos
# ---------------------------------------------------------------------------
@app.websocket("/ws/eco")
async def eco(websocket: WebSocket) -> None:
    await websocket.accept()  # "handshake": o HTTP é promovido a WebSocket
    await websocket.send_text("Conectado! Escreva algo e eu repito.")
    try:
        while True:
            texto = await websocket.receive_text()  # espera o cliente falar
            await websocket.send_text(
                f"[{datetime.now():%H:%M:%S}] você disse: {texto}"
            )
    except WebSocketDisconnect:
        print("Cliente desconectou")


# ---------------------------------------------------------------------------
# Página de teste (cliente em JavaScript)
# ---------------------------------------------------------------------------
PAGINA = """
<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>Eco WebSocket</title></head>
<body style="font-family:sans-serif;max-width:560px;margin:2rem auto">
  <h2>Eco via WebSocket</h2>
  <input id="texto" placeholder="mensagem" style="width:70%">
  <button onclick="enviar()">Enviar</button>
  <ul id="log"></ul>
  <script>
    const ws = new WebSocket(`ws://${location.host}/ws/eco`);
    ws.onmessage = (e) => {
      const li = document.createElement("li");
      li.textContent = e.data;
      document.getElementById("log").appendChild(li);
    };
    function enviar() {
      const campo = document.getElementById("texto");
      ws.send(campo.value);
      campo.value = "";
    }
  </script>
</body></html>
"""


@app.get("/", response_class=HTMLResponse)
async def pagina() -> str:
    return PAGINA
