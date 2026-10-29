"""Chat em tempo real de cada chamado (WebSocket).

Conexão:  ws://127.0.0.1:8000/ws/tickets/{ticket_id}?token=<JWT>        (suporte)
          ws://127.0.0.1:8000/ws/tickets/{ticket_id}?email=<e-mail>     (cliente)

Mensagens recebidas do cliente: texto puro.
Mensagens enviadas pelo servidor: JSON, ex.:
    {"tipo": "mensagem", "autor": "...", "texto": "...", "enviada_em": "..."}
    {"tipo": "historico", "mensagens": [...]}
    {"tipo": "sistema", "texto": "... entrou no chat"}
"""

from pathlib import Path
from typing import Annotated

from app.core.security import decodificar_token
from app.dependencies import TicketServiceDep
from app.models.ticket import Ticket
from app.services import agente_service
from app.services.chat_manager import ConnectionManager, get_chat_manager
from app.services.ticket_service import TicketNotFoundError
from beanie import PydanticObjectId
from fastapi import (
    APIRouter,
    Depends,
    Query,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi.responses import FileResponse

router = APIRouter(tags=["Chat"])

ChatManagerDep = Annotated[ConnectionManager, Depends(get_chat_manager)]

PAGINA_CHAT = Path(__file__).resolve().parent.parent / "static" / "chat.html"
MAX_TAMANHO_MENSAGEM = 1000


@router.get("/chat", include_in_schema=False)
async def pagina_do_chat() -> FileResponse:
    """Cliente web simples para testar o chat no navegador."""
    return FileResponse(PAGINA_CHAT)


async def identificar_autor(
    ticket: Ticket, token: str | None, email: str | None
) -> str | None:
    """Descobre quem está entrando. Devolve o nome de exibição ou None (negado)."""
    if token:  # atendente: o token JWT precisa ser válido
        email_agente = decodificar_token(token)
        agente = await agente_service.buscar_por_email(email_agente or "")
        if agente is not None and agente.ativo:
            return f"suporte ({agente.nome})"
        return None
    if email and email.lower() == ticket.email_solicitante.lower():
        return ticket.email_solicitante  # cliente dono do chamado
    return None


@router.websocket("/ws/tickets/{ticket_id}")
async def chat_do_chamado(
    websocket: WebSocket,
    ticket_id: PydanticObjectId,
    service: TicketServiceDep,
    manager: ChatManagerDep,
    token: Annotated[str | None, Query()] = None,
    email: Annotated[str | None, Query()] = None,
) -> None:
    # 1. O chamado existe? Quem está pedindo para entrar pode participar?
    try:
        ticket = await service.buscar(ticket_id)
    except TicketNotFoundError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    autor = await identificar_autor(ticket, token, email)
    if autor is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # 2. Entra na sala e recebe o histórico
    sala = str(ticket_id)
    await manager.conectar(sala, websocket)
    historico = [
        {
            "autor": m.autor,
            "texto": m.texto,
            "enviada_em": m.enviada_em.isoformat(),
        }
        for m in ticket.mensagens
    ]
    await manager.enviar_pessoal(
        websocket, {"tipo": "historico", "mensagens": historico}
    )
    await manager.transmitir(
        sala, {"tipo": "sistema", "texto": f"{autor} entrou no chat"}
    )

    # 3. Loop: recebe texto -> salva no banco -> transmite para a sala
    try:
        while True:
            texto = (await websocket.receive_text()).strip()
            if not texto:
                continue
            texto = texto[:MAX_TAMANHO_MENSAGEM]
            mensagem = await service.adicionar_mensagem(ticket_id, autor, texto)
            await manager.transmitir(
                sala,
                {
                    "tipo": "mensagem",
                    "autor": mensagem.autor,
                    "texto": mensagem.texto,
                    "enviada_em": mensagem.enviada_em.isoformat(),
                },
            )
    except WebSocketDisconnect:
        manager.desconectar(sala, websocket)
        await manager.transmitir(
            sala, {"tipo": "sistema", "texto": f"{autor} saiu do chat"}
        )
