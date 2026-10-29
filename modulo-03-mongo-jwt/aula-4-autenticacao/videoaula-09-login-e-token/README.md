# Videoaula 9 — Gerando e entregando o Token JWT no fluxo de login do atendente (14 min)

**Objetivo:** cadastrar um atendente (com hash de senha), fazer login e receber o token JWT.

**Arquivos**
- [`models.py`](models.py): `Agente` (campo `senha_hash`).
- [`security.py`](security.py): `gerar_hash_senha`, `verificar_senha`, `criar_token_acesso`, `decodificar_token`.
- [`criar_agente.py`](criar_agente.py): script para cadastrar o atendente.
- [`main.py`](main.py): `POST /auth/login`.
- [`schemas.py`](schemas.py), [`config.py`](config.py), [`database.py`](database.py).

## Como rodar
```powershell
pip install -r requirements.txt
copy .env.example .env        # preencha MONGO_URI e gere a SECRET_KEY
python criar_agente.py "Ana Souza" ana@helpdesk.com
uvicorn main:app --reload
```
No Swagger, clique em **Authorize** (ou use `POST /auth/login`) com `username` = e-mail e `password` = a senha.
A resposta traz `access_token`: cole em <https://jwt.io> para ver o payload.

## Roteiro de gravação
1. Cadastrar o atendente e mostrar o documento no Atlas: só existe `senha_hash`.
2. `POST /auth/login`: buscar o atendente, conferir a senha com `verificar_senha`.
3. Erro 401 com mensagem **genérica** (não revelar se o e-mail existe).
4. `criar_token_acesso`: claims `sub`, `iat`, `exp`. Tempo de vida curto.
5. Resposta no padrão OAuth2: `{"access_token": "...", "token_type": "bearer"}`.
6. Mostrar o fluxo com senha errada, atendente inativo e senha certa.
