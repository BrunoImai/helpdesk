"""
VIDEOAULA 1 — O mesmo chamado em SQL (tabelas) e em documento (NoSQL).

Execute:  python sql_vs_documento.py
"""

import json
import sqlite3

# ---------------------------------------------------------------------------
# 1. SQL: o chamado é "espalhado" em várias tabelas
# ---------------------------------------------------------------------------
print("=== 1. SQL (SQLite em memória) ===")
conn = sqlite3.connect(":memory:")
conn.executescript("""
    CREATE TABLE tickets   (id INTEGER PRIMARY KEY, titulo TEXT, status TEXT);
    CREATE TABLE mensagens (id INTEGER PRIMARY KEY, ticket_id INTEGER, autor TEXT, texto TEXT,
                            FOREIGN KEY (ticket_id) REFERENCES tickets(id));
    CREATE TABLE tags      (ticket_id INTEGER, tag TEXT);

    INSERT INTO tickets   VALUES (1, 'VPN não conecta', 'aberto');
    INSERT INTO mensagens (ticket_id, autor, texto) VALUES
        (1, 'cliente', 'Não consigo conectar'),
        (1, 'suporte', 'Qual erro aparece?'),
        (1, 'cliente', 'Erro 809');
    INSERT INTO tags VALUES (1, 'vpn'), (1, 'rede');
    """)

# Para montar UM chamado completo, precisamos de consultas/JOINs em 3 tabelas
ticket = conn.execute("SELECT * FROM tickets WHERE id = 1").fetchone()
mensagens = conn.execute(
    "SELECT autor, texto FROM mensagens WHERE ticket_id = 1 ORDER BY id"
).fetchall()
tags = [t[0] for t in conn.execute("SELECT tag FROM tags WHERE ticket_id = 1")]
print("Consultas necessárias: 3 (tickets, mensagens, tags)")
print({"id": ticket[0], "titulo": ticket[1], "mensagens": mensagens, "tags": tags})

# Evoluir o esquema (campo novo) exige alterar a tabela
conn.execute("ALTER TABLE tickets ADD COLUMN codigo_erro TEXT")
print("Para guardar o 'codigo_erro' foi preciso um ALTER TABLE (migração).\n")

# ---------------------------------------------------------------------------
# 2. Documento: o chamado é UM objeto só (é assim que o MongoDB guarda)
# ---------------------------------------------------------------------------
print("=== 2. Documento (estilo MongoDB) ===")
documento = {
    "_id": "64b7f0c2a1b2c3d4e5f60718",
    "titulo": "VPN não conecta",
    "status": "aberto",
    "tags": ["vpn", "rede"],
    "mensagens": [
        {"autor": "cliente", "texto": "Não consigo conectar"},
        {"autor": "suporte", "texto": "Qual erro aparece?"},
        {"autor": "cliente", "texto": "Erro 809"},
    ],
    # Campo extra só neste chamado: nenhuma migração necessária
    "codigo_erro": "809",
}
print("Leituras necessárias: 1 (o documento já vem completo)")
print(json.dumps(documento, indent=2, ensure_ascii=False))
