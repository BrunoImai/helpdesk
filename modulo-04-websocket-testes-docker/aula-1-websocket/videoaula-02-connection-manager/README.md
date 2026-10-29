# Videoaula 2 — Criando o Connection Manager (12 min)

**Objetivo:** construir a classe que controla as conexões abertas e distribui mensagens por sala.

**Arquivos:** [`main.py`](main.py) (versão didática, sem banco). A versão final, com salas por chamado e
mensagens gravadas no MongoDB, está em `projeto-final/app/services/chat_manager.py`.

## Como rodar
```powershell
pip install fastapi "uvicorn[standard]"
uvicorn main:app --reload
```
Abra <http://127.0.0.1:8000/> em duas abas (mesma sala, nomes diferentes) e converse. Veja `GET /salas`.

## Roteiro de gravação
1. Por que o `/ws/eco` não basta: cada conexão é uma ilha.
2. `ConnectionManager`: `conectar` (accept + guardar), `desconectar`, `transmitir` (broadcast).
3. **Uma única instância** compartilhada (`manager = ConnectionManager()`).
4. Salas: um dicionário `sala -> [conexões]` (no HelpDesk, a sala é o id do chamado).
5. Limite do exemplo: a memória pertence a **um** processo. Com vários workers, é preciso Redis Pub/Sub (Videoaula 8).
