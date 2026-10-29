"""Envio de e-mails (simulado) para ser usado em tarefas de fundo."""

import asyncio
import logging

logger = logging.getLogger("helpdesk.email")


async def enviar_email_confirmacao(destino: str, ticket_id: str) -> None:
    """Simula o envio de um e-mail (leva ~2 segundos)."""
    logger.info("Enviando e-mail de confirmação para %s ...", destino)
    await asyncio.sleep(2)  # no mundo real: chamada a um servidor SMTP / API
    logger.info("E-mail enviado para %s (chamado %s)", destino, ticket_id)
