# Videoaula 2 — Coleções e Documentos: modelando os chamados (12 min)

**Objetivo:** aprender o vocabulário do MongoDB (banco, coleção, documento, `_id`) e decidir entre **embutir** ou **referenciar** dados.

| SQL | MongoDB |
|---|---|
| Banco de dados | Banco de dados (`helpdesk`) |
| Tabela | Coleção (`tickets`, `agentes`) |
| Linha | Documento (JSON/BSON) |
| Coluna | Campo |
| Chave primária | `_id` (`ObjectId`) |
| `JOIN` | Documento embutido ou referência |

**Arquivos**
- [`chamado_exemplo.json`](chamado_exemplo.json): documento de um chamado.
- [`modelagem.py`](modelagem.py): modelos Pydantic com mensagens **embutidas** e atendente **referenciado**.
- [`consultas_mongosh.md`](consultas_mongosh.md): comandos `mongosh` para mostrar as operações básicas.

## Como rodar
```powershell
python modelagem.py
```

## Roteiro de gravação
1. Abrir `chamado_exemplo.json` e mapear cada parte (campos simples, lista de tags, lista de mensagens).
2. Regra prática: **embutir** quando os dados são lidos juntos e pertencem a um só pai (mensagens do chamado);
   **referenciar** quando a entidade vive por si só e é compartilhada (o atendente).
3. Cuidado com listas que crescem sem limite (documento tem teto de 16 MB).
4. Rodar `modelagem.py` e mostrar como o Pydantic representa o documento.
5. Mostrar as consultas no `mongosh` / Atlas (Data Explorer).
