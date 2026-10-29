"""
VIDEOAULA 7 — Senhas seguras: Hashing x Criptografia.

- HASH: caminho de MÃO ÚNICA. Não existe "desfazer". Serve para guardar senhas.
- CRIPTOGRAFIA: caminho de MÃO DUPLA (com chave). Serve para proteger dados que
  precisam ser lidos de novo (ex.: um documento sigiloso).

Execute:  python hashing_vs_criptografia.py
Requer:   pip install bcrypt cryptography
"""

import hashlib
import time

import bcrypt
from cryptography.fernet import Fernet

SENHA = "MinhaSenha@123"

# ---------------------------------------------------------------------------
# 1. Senha em texto puro: NUNCA
# ---------------------------------------------------------------------------
print("=== 1. Texto puro (o que NÃO fazer) ===")
print(f"No banco: {SENHA}  <- qualquer vazamento expõe todas as senhas\n")

# ---------------------------------------------------------------------------
# 2. Hash rápido (SHA-256): melhor que nada, mas ainda inadequado para senhas
# ---------------------------------------------------------------------------
print("=== 2. SHA-256 (hash rápido) ===")
sha = hashlib.sha256(SENHA.encode()).hexdigest()
print(f"Hash: {sha}")
print(
    "Sempre igual para a mesma senha ->",
    sha == hashlib.sha256(SENHA.encode()).hexdigest(),
)
print(
    "Problema: é MUITO rápido e sem 'sal'; tabelas prontas (rainbow tables) quebram senhas comuns.\n"
)

# ---------------------------------------------------------------------------
# 3. bcrypt: hash lento + sal aleatório (o padrão para senhas)
# ---------------------------------------------------------------------------
print("=== 3. bcrypt (hash apropriado para senhas) ===")
hash1 = bcrypt.hashpw(SENHA.encode(), bcrypt.gensalt())
hash2 = bcrypt.hashpw(SENHA.encode(), bcrypt.gensalt())
print(f"Hash 1: {hash1.decode()}")
print(f"Hash 2: {hash2.decode()}")
print("Mesma senha, hashes DIFERENTES (cada um tem um sal aleatório):", hash1 != hash2)

print("Verificando a senha correta :", bcrypt.checkpw(SENHA.encode(), hash1))
print("Verificando a senha errada  :", bcrypt.checkpw(b"outra-senha", hash1))

inicio = time.perf_counter()
bcrypt.hashpw(SENHA.encode(), bcrypt.gensalt(rounds=12))
print(
    f"Custo proposital: gerar um hash leva ~{time.perf_counter() - inicio:.2f}s (rounds=12)\n"
)

# Anatomia do hash:  $2b$12$<22 caracteres de sal><31 caracteres do hash>
algoritmo, custo, resto = hash1.decode().split("$")[1:]
print(
    f"Anatomia -> algoritmo: {algoritmo} | custo: {custo} | sal+hash: {resto[:22]}...\n"
)

# ---------------------------------------------------------------------------
# 4. Criptografia (Fernet): dá para DECIFRAR com a chave
# ---------------------------------------------------------------------------
print("=== 4. Criptografia simétrica (Fernet) ===")
chave = Fernet.generate_key()
cofre = Fernet(chave)
cifrado = cofre.encrypt(SENHA.encode())
print(f"Cifrado   : {cifrado.decode()[:60]}...")
print(f"Decifrado : {cofre.decrypt(cifrado).decode()}   <- reversível com a chave")
print(
    "Por isso NÃO se usa criptografia para guardar senhas: quem roubar a chave lê todas."
)

# ---------------------------------------------------------------------------
# Resumo
# ---------------------------------------------------------------------------
print("""
Resumo
  Hash (bcrypt/argon2) : senhas  | mão única | comparamos hash com hash
  Criptografia (Fernet): dados   | mão dupla | precisa guardar a chave com segurança
""")
