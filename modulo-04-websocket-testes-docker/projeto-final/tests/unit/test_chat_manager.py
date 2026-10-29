"""TESTES DE UNIDADE: ConnectionManager (usa um WebSocket "de mentira")."""

from typing import Any

from app.services.chat_manager import ConnectionManager


class WebSocketFalso:
    """Imita só o que o ConnectionManager usa de um WebSocket real."""

    def __init__(self, quebrado: bool = False) -> None:
        self.aceito = False
        self.recebidas: list[dict[str, Any]] = []
        self.quebrado = quebrado

    async def accept(self) -> None:
        self.aceito = True

    async def send_json(self, dados: dict[str, Any]) -> None:
        if self.quebrado:
            raise RuntimeError("conexão caiu")
        self.recebidas.append(dados)


async def test_conectar_aceita_e_registra_na_sala() -> None:
    manager = ConnectionManager()
    ws = WebSocketFalso()
    await manager.conectar("sala-1", ws)  # type: ignore[arg-type]
    assert ws.aceito
    assert manager.total_na_sala("sala-1") == 1


async def test_transmitir_chega_so_para_quem_esta_na_sala() -> None:
    manager = ConnectionManager()
    a, b, de_outra_sala = WebSocketFalso(), WebSocketFalso(), WebSocketFalso()
    await manager.conectar("sala-1", a)  # type: ignore[arg-type]
    await manager.conectar("sala-1", b)  # type: ignore[arg-type]
    await manager.conectar("sala-2", de_outra_sala)  # type: ignore[arg-type]

    await manager.transmitir("sala-1", {"texto": "olá"})

    assert a.recebidas == [{"texto": "olá"}]
    assert b.recebidas == [{"texto": "olá"}]
    assert de_outra_sala.recebidas == []


async def test_desconectar_remove_e_apaga_sala_vazia() -> None:
    manager = ConnectionManager()
    ws = WebSocketFalso()
    await manager.conectar("sala-1", ws)  # type: ignore[arg-type]
    manager.desconectar("sala-1", ws)  # type: ignore[arg-type]
    assert manager.total_na_sala("sala-1") == 0


async def test_conexao_quebrada_e_removida_sem_derrubar_os_outros() -> None:
    manager = ConnectionManager()
    quebrado, saudavel = WebSocketFalso(quebrado=True), WebSocketFalso()
    await manager.conectar("sala-1", quebrado)  # type: ignore[arg-type]
    await manager.conectar("sala-1", saudavel)  # type: ignore[arg-type]

    await manager.transmitir("sala-1", {"texto": "teste"})

    assert saudavel.recebidas == [{"texto": "teste"}]
    assert manager.total_na_sala("sala-1") == 1
