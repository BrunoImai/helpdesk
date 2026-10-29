# Videoaula 1 — Por que o SQL não é a melhor escolha para um histórico de chat? (10 min)

**Objetivo:** comparar, na prática, guardar um chamado com histórico de mensagens em tabelas (SQL) e em um documento (NoSQL).

**Arquivos**
- [`sql_vs_documento.py`](sql_vs_documento.py): usa `sqlite3` (já vem no Python) e um `dict` JSON-like para mostrar as duas formas.

## Como rodar
```powershell
python sql_vs_documento.py
```

## Roteiro de gravação
1. Rodar o script: o mesmo chamado em SQL (3 tabelas + `JOIN`) e em documento (1 estrutura).
2. Mostrar que o chamado e suas mensagens são lidos **juntos**; no documento, é uma única leitura.
3. Mostrar a flexibilidade: um chamado de "VPN" tem campos extras que os outros não têm (sem `ALTER TABLE`).
4. Quando **SQL** ainda é melhor: relações complexas, transações entre várias entidades, relatórios com muitos `JOIN`.
5. Quando **NoSQL (documentos)** brilha: dados semiestruturados, leitura de "tudo junto", evolução rápida do esquema.

| | SQL | MongoDB (documentos) |
|---|---|---|
| Estrutura | Tabelas e colunas fixas | Documentos BSON flexíveis |
| Relacionamentos | `JOIN` | Dados embutidos ou referências |
| Evolução do esquema | `ALTER TABLE`/migrações | Basta salvar o campo novo |
| Ideal para | Dados altamente relacionais | Histórico de chat, catálogos, logs |
