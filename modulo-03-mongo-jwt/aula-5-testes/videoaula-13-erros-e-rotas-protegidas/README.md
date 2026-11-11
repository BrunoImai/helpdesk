# Videoaula 13 — Testando erros e rotas protegidas (14 min)

**Objetivo:** provar que a API **recusa** o que deve recusar (422 e 401), não só que funciona no caminho feliz.

**Arquivo:** [`test_erros_e_rotas_protegidas.py`](test_erros_e_rotas_protegidas.py): testa a API do `projeto-final`
do Módulo 3 **sem banco de dados**. A versão do projeto está em `projeto-final/tests/test_main.py`.

## Como rodar
```powershell
cd modulo-03-mongo-jwt\projeto-final
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd ..\aula-5-testes\videoaula-13-erros-e-rotas-protegidas
pytest test_erros_e_rotas_protegidas.py
```
Esperado: `7 passed`.

## Por que não precisa de banco?
O teste usa `TestClient(app)` **sem** `with`, então o `lifespan` (que conecta no MongoDB) não roda. E os erros testados
acontecem **antes** do banco: o Pydantic valida o corpo (422) e a dependência de autenticação rejeita o pedido (401).

| Situação | Esperado |
|---|---|
| E-mail inválido ao abrir chamado | `422` |
| Título com tipo errado (número no lugar de texto) | `422` |
| `GET /tickets` sem token | `401` + cabeçalho `WWW-Authenticate: Bearer` |
| Token falso | `401` |
| Outras rotas do suporte (`parametrize`) | `401` |

## Caminho feliz x caminho de erro
- **Caminho feliz:** o usuário faz tudo certo (e-mail válido, token válido) e a API responde 200/201.
- **Caminho de erro:** o usuário erra (ou ataca) e a API precisa dizer *não* do jeito certo (status e mensagem).
Um sistema só é confiável se os dois estiverem cobertos por testes.

## Roteiro de gravação
1. Exemplo do dia a dia: o caixa eletrônico também precisa ser testado com senha errada.
2. Escrever o teste do 422 (e-mail inválido) e rodar.
3. Escrever o teste do 401 (sem token) e rodar.
4. **Quebrar de propósito:** remover o `Depends(get_agente_atual)` de uma rota em `app/routers/tickets.py` e ver o teste ficar vermelho (depois desfaça a mudança).
5. Mostrar o `parametrize` cobrindo várias rotas de uma vez.
