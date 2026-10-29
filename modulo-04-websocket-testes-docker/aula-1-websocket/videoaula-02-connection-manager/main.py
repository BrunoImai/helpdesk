"""
VIDEOAULA 2 — Criando o Connection Manager.

Problema: com `/ws/eco` cada conexão só conversa consigo mesma. Para um CHAT,
precisamos saber QUEM está conectado e repassar mensagens para todos de uma sala.

Execute:  uvicorn main:app --reload
Abra DUAS abas em  http://127.0.0.1:8000/  e converse entre elas.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI(title="HelpDesk — Connection Manager")


# ---------------------------------------------------------------------------
# >>> DEMONSTRAÇÃO: o Connection Manager
# ---------------------------------------------------------------------------
class ConnectionManager:
    def __init__(self) -> None:
        # sala -> lista de conexões abertas naquela sala
        self.salas: dict[str, list[WebSocket]] = {}

    async def conectar(self, sala: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.salas.setdefault(sala, []).append(websocket)

    def desconectar(self, sala: str, websocket: WebSocket) -> None:
        self.salas[sala].remove(websocket)
        if not self.salas[sala]:
            del self.salas[sala]  # sala vazia some

    async def transmitir(self, sala: str, mensagem: str) -> None:
        for conexao in self.salas.get(sala, []):
            await conexao.send_text(mensagem)


manager = ConnectionManager()  # UMA instância compartilhada por todas as conexões


@app.websocket("/ws/{sala}/{nome}")
async def chat(websocket: WebSocket, sala: str, nome: str) -> None:
    await manager.conectar(sala, websocket)
    await manager.transmitir(sala, f"* {nome} entrou na sala {sala}")
    try:
        while True:
            texto = await websocket.receive_text()
            await manager.transmitir(sala, f"{nome}: {texto}")
    except WebSocketDisconnect:
        manager.desconectar(sala, websocket)
        await manager.transmitir(sala, f"* {nome} saiu")


@app.get("/salas")
async def salas() -> dict[str, int]:
    """Quantas pessoas há em cada sala agora."""
    return {sala: len(conexoes) for sala, conexoes in manager.salas.items()}


PAGINA = """
<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>Chat simples</title></head>
<body style="font-family:sans-serif;max-width:560px;margin:2rem auto">
  <h2>Chat simples (Connection Manager)</h2>
  <input id="nome" placeholder="seu nome" value="Visitante">
  <input id="sala" placeholder="sala" value="chamado-1">
  <button onclick="entrar()">Entrar</button>
  <ul id="log"></ul>
  <input id="texto" placeholder="mensagem" style="width:70%">
  <button onclick="enviar()">Enviar</button>
  <script>
    let ws;
    function entrar() {
      const nome = encodeURIComponent(document.getElementById("nome").value);
      const sala = encodeURIComponent(document.getElementById("sala").value);
      ws = new WebSocket(`ws://${location.host}/ws/${sala}/${nome}`);
      ws.onmessage = (e) => {
        const li = document.createElement("li");
        li.textContent = e.data;
        document.getElementById("log").appendChild(li);
      };
    }
    function enviar() {
      const campo = document.getElementById("texto");
      if (ws) ws.send(campo.value);
      campo.value = "";
    }
  </script>
</body></html>
"""


@app.get("/", response_class=HTMLResponse)
async def pagina() -> str:
    return PAGINA
