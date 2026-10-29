"""Connection Manager: controla quem está conectado em cada sala de chat.

Cada chamado é uma "sala" (o id do chamado). Quando alguém escreve, o gerenciador
repassa a mensagem para todos os conectados naquela sala.

Observação: o estado fica na memória de UM processo. Com vários workers/servidores
seria necessário um intermediário (ex.: Redis Pub/Sub) para sincronizá-los.
"""

from collections import defaultdict
from functools import lru_cache
from typing import Any

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self._salas: dict[str, list[WebSocket]] = defaultdict(list)

    async def conectar(self, sala: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self._salas[sala].append(websocket)

    def desconectar(self, sala: str, websocket: WebSocket) -> None:
        conexoes = self._salas.get(sala, [])
        if websocket in conexoes:
            conexoes.remove(websocket)
        if not conexoes:
            self._salas.pop(sala, None)  # sala vazia deixa de existir

    def total_na_sala(self, sala: str) -> int:
        return len(self._salas.get(sala, []))

    async def enviar_pessoal(self, websocket: WebSocket, dados: dict[str, Any]) -> None:
        await websocket.send_json(dados)

    async def transmitir(self, sala: str, dados: dict[str, Any]) -> None:
        """Envia a mensagem a todos da sala (remove quem já caiu)."""
        for conexao in list(self._salas.get(sala, [])):
            try:
                await conexao.send_json(dados)
            except Exception:  # conexão quebrada: tira da sala
                self.desconectar(sala, conexao)


@lru_cache
def get_chat_manager() -> ConnectionManager:
    """Instância única durante a vida da aplicação."""
    return ConnectionManager()
