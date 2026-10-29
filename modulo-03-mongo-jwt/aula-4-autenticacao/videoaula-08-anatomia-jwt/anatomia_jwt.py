"""
VIDEOAULA 8 — Como funciona a autenticação via Tokens JWT.

Um JWT tem 3 partes separadas por ponto:  HEADER.PAYLOAD.SIGNATURE
  - header   : algoritmo e tipo do token
  - payload  : os "claims" (sub = quem é, exp = quando expira...)
  - signature: assinatura que garante que ninguém alterou o conteúdo

ATENÇÃO: o payload é apenas codificado em Base64, NÃO é secreto!

Execute:  python anatomia_jwt.py
Requer:   pip install pyjwt
"""

import base64
import json
import time
from datetime import UTC, datetime, timedelta

import jwt

CHAVE_SECRETA = "chave-de-demonstracao-nao-use-em-producao-0123456789"


def decodificar_parte(parte: str) -> dict[str, object]:
    """Decodifica uma parte Base64URL do token SEM precisar da chave."""
    parte += "=" * (-len(parte) % 4)  # restaura o padding removido
    return json.loads(base64.urlsafe_b64decode(parte))


# ---------------------------------------------------------------------------
# 1. Criando um token
# ---------------------------------------------------------------------------
print("=== 1. Criando o token ===")
agora = datetime.now(UTC)
payload = {
    "sub": "ana@helpdesk.com",  # subject: quem é o dono do token
    "iat": agora,  # issued at: emitido em
    "exp": agora + timedelta(seconds=2),  # expiration: expira em 2 s (demo)
}
token = jwt.encode(payload, CHAVE_SECRETA, algorithm="HS256")
print(token, "\n")

# ---------------------------------------------------------------------------
# 2. Dissecando as 3 partes
# ---------------------------------------------------------------------------
print("=== 2. As 3 partes ===")
header, corpo, assinatura = token.split(".")
print("HEADER   :", decodificar_parte(header))
print("PAYLOAD  :", decodificar_parte(corpo), " <- qualquer um consegue ler!")
print("SIGNATURE:", assinatura, " <- só quem tem a chave consegue gerar\n")

# ---------------------------------------------------------------------------
# 3. Validando
# ---------------------------------------------------------------------------
print("=== 3. Validação ===")
dados = jwt.decode(token, CHAVE_SECRETA, algorithms=["HS256"])
print("Token válido. Dono:", dados["sub"], "\n")

# ---------------------------------------------------------------------------
# 4. Tentativa de fraude: trocar o payload mantendo a assinatura
# ---------------------------------------------------------------------------
print("=== 4. Adulteração do payload ===")
payload_falso = {**decodificar_parte(corpo), "sub": "admin@helpdesk.com"}
corpo_falso = base64.urlsafe_b64encode(json.dumps(payload_falso).encode()).rstrip(b"=")
token_adulterado = f"{header}.{corpo_falso.decode()}.{assinatura}"
try:
    jwt.decode(token_adulterado, CHAVE_SECRETA, algorithms=["HS256"])
except jwt.InvalidSignatureError:
    print("Rejeitado: assinatura inválida (o payload foi alterado)\n")

# ---------------------------------------------------------------------------
# 5. Chave errada
# ---------------------------------------------------------------------------
print("=== 5. Chave errada ===")
try:
    jwt.decode(
        token, "outra-chave-qualquer-com-mais-de-32-caracteres", algorithms=["HS256"]
    )
except jwt.InvalidSignatureError:
    print("Rejeitado: assinado com outra chave\n")

# ---------------------------------------------------------------------------
# 6. Expiração
# ---------------------------------------------------------------------------
print("=== 6. Expiração (aguardando 3 s...) ===")
time.sleep(3)
try:
    jwt.decode(token, CHAVE_SECRETA, algorithms=["HS256"])
except jwt.ExpiredSignatureError:
    print("Rejeitado: o token expirou")
