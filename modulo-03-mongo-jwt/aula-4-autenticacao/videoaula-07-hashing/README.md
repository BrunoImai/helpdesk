# Videoaula 7 — Senhas seguras: hashing e as regras básicas de criptografia Web (8 min)

**Objetivo:** entender por que **nunca** guardamos senhas em texto puro e como o bcrypt protege os dados.

**Arquivos**
- [`hashing_vs_criptografia.py`](hashing_vs_criptografia.py): texto puro x SHA-256 x bcrypt x criptografia (Fernet).

| | Hash (bcrypt) | Criptografia (Fernet/AES) |
|---|---|---|
| Reversível? | **Não** | Sim, com a chave |
| Usado para | Verificar senhas | Proteger dados que precisam ser lidos depois |
| "Sal" (salt) | Aleatório, embutido no hash | Não se aplica |
| Como confere | `checkpw(senha, hash)` | `decrypt(token)` |

## Como rodar
```powershell
pip install bcrypt cryptography
python hashing_vs_criptografia.py
```

## Roteiro de gravação
1. Mostrar o desastre: banco vazado com senhas em texto puro.
2. SHA-256: rápido demais, mesma senha = mesmo hash.
3. bcrypt: sal aleatório (dois hashes diferentes para a mesma senha) e custo configurável.
4. `checkpw`: como o login confere a senha sem nunca "descobrir" a original.
5. Criptografia (Fernet): reversível. Diferença conceitual para o hash.
6. Regras básicas: HTTPS sempre, nunca logar senhas, exigir senha forte, não inventar o seu próprio algoritmo.

> No projeto final, estas funções ficam em `app/core/security.py` (`gerar_hash_senha` e `verificar_senha`).
