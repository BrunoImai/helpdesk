# Videoaula 5 — Compartilhando recursos com Injeção de Dependências (`Depends`) (12 min)

**Objetivo:** reaproveitar lógica (paginação, serviço, configuração) entre rotas usando `Depends`.

**Arquivos:** [`main.py`](main.py)

## Como rodar
```powershell
pip install fastapi "uvicorn[standard]"
uvicorn main:app --reload
```
Teste: `/tickets?skip=0&limit=2`, `/tickets/1` e `/admin/resumo` com e sem o cabeçalho `x-api-key: segredo-do-helpdesk`.

## Roteiro de gravação
1. Problema: `skip` e `limit` repetidos em várias rotas.
2. Função de dependência `paginacao()` + `Depends(paginacao)`.
3. Dependência como **classe** (`Paginacao`) e `Annotated[..., Depends()]` para reutilizar o tipo.
4. Dependência de **serviço** (`get_ticket_service`), a base para trocar a implementação nos testes (Módulo 4).
5. Dependência que **bloqueia** a rota (`verificar_chave`): preparação para a autenticação JWT do Módulo 3.
6. Dependências podem depender de outras dependências.
