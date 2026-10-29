# Trilha Dominando Python para Web — Código do HelpDesk

Código de apoio às videoaulas da trilha. Cada videoaula que precisa de código tem sua própria pasta
(`videoaula-XX-...`) com um `README.md` (objetivo, como rodar e roteiro de gravação) e os arquivos novos
ou alterados naquele ponto. Ao final de cada módulo existe a pasta `projeto-final/` com o estado completo
e executável do HelpDesk.

## Como usar

```powershell
# Na raiz do repositório (uma vez)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

Para executar um módulo, entre em `modulo-XX-.../projeto-final` e siga o `README.md` de lá.
Os scripts de videoaula (arquivos `.py` soltos) rodam direto: `python caminho/do/arquivo.py`.

## Índice

### Módulo 00 — Teste de proficiência
| Pasta | Conteúdo |
|---|---|
| [`modulo-00-diagnostico`](modulo-00-diagnostico) | Exercícios de código usados como base das questões do diagnóstico |

### Módulo 1 — O Alicerce (Git, ambiente, tipagem, Pydantic)
| Aula | Videoaula | Pasta |
|---|---|---|
| 1 Git e GitHub | V1 Introdução ao Git e branches | [`aula-1-git/videoaula-01-intro-git`](modulo-01-alicerce/aula-1-git/videoaula-01-intro-git) |
| 1 Git e GitHub | V2 Repositórios remotos e boas práticas | [`aula-1-git/videoaula-02-remotos-boas-praticas`](modulo-01-alicerce/aula-1-git/videoaula-02-remotos-boas-praticas) |
| 2 Ambientes e qualidade | V3 `venv` / Poetry | [`aula-2-ambientes/videoaula-03-ambientes-virtuais`](modulo-01-alicerce/aula-2-ambientes/videoaula-03-ambientes-virtuais) |
| 2 Ambientes e qualidade | V4 Linters, formatters e `.env` | [`aula-2-ambientes/videoaula-04-qualidade-e-env`](modulo-01-alicerce/aula-2-ambientes/videoaula-04-qualidade-e-env) |
| 3 Tipagem moderna | V5 Type hints | [`aula-3-tipagem/videoaula-05-type-hints`](modulo-01-alicerce/aula-3-tipagem/videoaula-05-type-hints) |
| 3 Tipagem moderna | V6 Coleções e opcionais | [`aula-3-tipagem/videoaula-06-colecoes-e-opcionais`](modulo-01-alicerce/aula-3-tipagem/videoaula-06-colecoes-e-opcionais) |
| 3 Tipagem moderna | V7 `Enum` e `Literal` | [`aula-3-tipagem/videoaula-07-enum-e-literal`](modulo-01-alicerce/aula-3-tipagem/videoaula-07-enum-e-literal) |
| 4 Pydantic | V8 Serialização | [`aula-4-pydantic/videoaula-08-serializacao`](modulo-01-alicerce/aula-4-pydantic/videoaula-08-serializacao) |
| 4 Pydantic | V9 `TicketCreate` | [`aula-4-pydantic/videoaula-09-ticket-create`](modulo-01-alicerce/aula-4-pydantic/videoaula-09-ticket-create) |
| 4 Pydantic | V10 Validadores customizados | [`aula-4-pydantic/videoaula-10-validadores`](modulo-01-alicerce/aula-4-pydantic/videoaula-10-validadores) |
| Avaliações | Gabaritos dos mini hands-on | [`avaliacoes`](modulo-01-alicerce/avaliacoes) |
| Desafio | Projeto final do módulo | [`projeto-final`](modulo-01-alicerce/projeto-final) |

### Módulo 2 — A API e o Atendimento Dinâmico (FastAPI e assíncrono)
| Aula | Videoaula | Pasta |
|---|---|---|
| 1 FastAPI e OpenAPI | V1 OpenAPI e FastAPI | [`aula-1-fastapi/videoaula-01-openapi-fastapi`](modulo-02-api/aula-1-fastapi/videoaula-01-openapi-fastapi) |
| 1 FastAPI e OpenAPI | V2 Camadas (Routers e Services) | [`aula-1-fastapi/videoaula-02-camadas`](modulo-02-api/aula-1-fastapi/videoaula-02-camadas) |
| 2 Endpoints REST | V3 Endpoints semânticos | [`aula-2-endpoints/videoaula-03-endpoints-rest`](modulo-02-api/aula-2-endpoints/videoaula-03-endpoints-rest) |
| 2 Endpoints REST | V4 Parâmetros e erros | [`aula-2-endpoints/videoaula-04-parametros-e-erros`](modulo-02-api/aula-2-endpoints/videoaula-04-parametros-e-erros) |
| 2 Endpoints REST | V5 `Depends` | [`aula-2-endpoints/videoaula-05-depends`](modulo-02-api/aula-2-endpoints/videoaula-05-depends) |
| 3 Concorrência | V6 Síncrono vs. assíncrono | [`aula-3-concorrencia/videoaula-06-sync-vs-async`](modulo-02-api/aula-3-concorrencia/videoaula-06-sync-vs-async) |
| 3 Concorrência | V7 WSGI vs. ASGI | [`aula-3-concorrencia/videoaula-07-wsgi-vs-asgi`](modulo-02-api/aula-3-concorrencia/videoaula-07-wsgi-vs-asgi) |
| 4 Assincronismo na prática | V8 `async/await` nas rotas | [`aula-4-async-pratica/videoaula-08-async-await-rotas`](modulo-02-api/aula-4-async-pratica/videoaula-08-async-await-rotas) |
| 4 Assincronismo na prática | V9 `BackgroundTasks` | [`aula-4-async-pratica/videoaula-09-background-tasks`](modulo-02-api/aula-4-async-pratica/videoaula-09-background-tasks) |
| Avaliações | Gabaritos | [`avaliacoes`](modulo-02-api/avaliacoes) |
| Desafio | Projeto final do módulo | [`projeto-final`](modulo-02-api/projeto-final) |

### Módulo 3 — Guardando Chamados e Trancando Portas (MongoDB e JWT)
| Aula | Videoaula | Pasta |
|---|---|---|
| 1 NoSQL | V1 SQL vs. NoSQL | [`aula-1-nosql/videoaula-01-sql-vs-nosql`](modulo-03-mongo-jwt/aula-1-nosql/videoaula-01-sql-vs-nosql) |
| 1 NoSQL | V2 Coleções e documentos | [`aula-1-nosql/videoaula-02-colecoes-e-documentos`](modulo-03-mongo-jwt/aula-1-nosql/videoaula-02-colecoes-e-documentos) |
| 2 FastAPI + MongoDB | V3 Motor e Beanie | [`aula-2-fastapi-mongo/videoaula-03-motor-beanie`](modulo-03-mongo-jwt/aula-2-fastapi-mongo/videoaula-03-motor-beanie) |
| 2 FastAPI + MongoDB | V4 Primeiro chamado real | [`aula-2-fastapi-mongo/videoaula-04-primeiro-chamado`](modulo-03-mongo-jwt/aula-2-fastapi-mongo/videoaula-04-primeiro-chamado) |
| 3 Operações avançadas | V5 CRUD completo | [`aula-3-operacoes-avancadas/videoaula-05-crud-completo`](modulo-03-mongo-jwt/aula-3-operacoes-avancadas/videoaula-05-crud-completo) |
| 3 Operações avançadas | V6 Filtros e agregações | [`aula-3-operacoes-avancadas/videoaula-06-filtros-e-agregacoes`](modulo-03-mongo-jwt/aula-3-operacoes-avancadas/videoaula-06-filtros-e-agregacoes) |
| 4 Autenticação | V7 Hashing de senhas | [`aula-4-autenticacao/videoaula-07-hashing`](modulo-03-mongo-jwt/aula-4-autenticacao/videoaula-07-hashing) |
| 4 Autenticação | V8 Anatomia do JWT | [`aula-4-autenticacao/videoaula-08-anatomia-jwt`](modulo-03-mongo-jwt/aula-4-autenticacao/videoaula-08-anatomia-jwt) |
| 4 Autenticação | V9 Login e emissão do token | [`aula-4-autenticacao/videoaula-09-login-e-token`](modulo-03-mongo-jwt/aula-4-autenticacao/videoaula-09-login-e-token) |
| 4 Autenticação | V10 Rotas protegidas | [`aula-4-autenticacao/videoaula-10-rotas-protegidas`](modulo-03-mongo-jwt/aula-4-autenticacao/videoaula-10-rotas-protegidas) |
| Avaliações | Gabaritos | [`avaliacoes`](modulo-03-mongo-jwt/avaliacoes) |
| Desafio | Projeto final do módulo | [`projeto-final`](modulo-03-mongo-jwt/projeto-final) |

### Módulo 4 — Tempo real, testes e deploy (WebSockets, Pytest e Docker)
| Aula | Videoaula | Pasta |
|---|---|---|
| 1 Tempo real | V1 WebSocket vs. HTTP | [`aula-1-websocket/videoaula-01-websocket-vs-http`](modulo-04-websocket-testes-docker/aula-1-websocket/videoaula-01-websocket-vs-http) |
| 1 Tempo real | V2 Connection Manager | [`aula-1-websocket/videoaula-02-connection-manager`](modulo-04-websocket-testes-docker/aula-1-websocket/videoaula-02-connection-manager) |
| 1 Tempo real | V3 Sala de chat do chamado | [`aula-1-websocket/videoaula-03-sala-de-chat`](modulo-04-websocket-testes-docker/aula-1-websocket/videoaula-03-sala-de-chat) |
| 2 Testes | V4 Pirâmide de testes | [`aula-2-testes/videoaula-04-piramide-de-testes`](modulo-04-websocket-testes-docker/aula-2-testes/videoaula-04-piramide-de-testes) |
| 2 Testes | V5 Pytest e TestClient | [`aula-2-testes/videoaula-05-pytest-testclient`](modulo-04-websocket-testes-docker/aula-2-testes/videoaula-05-pytest-testclient) |
| 3 Isolamento | V6 Mocks | [`aula-3-isolamento/videoaula-06-mocks`](modulo-04-websocket-testes-docker/aula-3-isolamento/videoaula-06-mocks) |
| 3 Isolamento | V7 Erros e rotas autenticadas | [`aula-3-isolamento/videoaula-07-erros-e-rotas-autenticadas`](modulo-04-websocket-testes-docker/aula-3-isolamento/videoaula-07-erros-e-rotas-autenticadas) |
| 4 Deploy | V8 Microsserviços e filas | [`aula-4-deploy/videoaula-08-microsservicos-e-filas`](modulo-04-websocket-testes-docker/aula-4-deploy/videoaula-08-microsservicos-e-filas) |
| 4 Deploy | V9 Containers | [`aula-4-deploy/videoaula-09-containers`](modulo-04-websocket-testes-docker/aula-4-deploy/videoaula-09-containers) |
| 4 Deploy | V10 Dockerfile | [`aula-4-deploy/videoaula-10-dockerfile`](modulo-04-websocket-testes-docker/aula-4-deploy/videoaula-10-dockerfile) |
| 4 Deploy | V11 Docker Compose | [`aula-4-deploy/videoaula-11-docker-compose`](modulo-04-websocket-testes-docker/aula-4-deploy/videoaula-11-docker-compose) |
| Avaliações | Gabaritos | [`avaliacoes`](modulo-04-websocket-testes-docker/avaliacoes) |
| Desafio | Projeto final do módulo | [`projeto-final`](modulo-04-websocket-testes-docker/projeto-final) |

## Convenções

- Todo arquivo de videoaula começa com um cabeçalho `VIDEOAULA X — título`.
- Trechos marcados com `# >>> DEMONSTRAÇÃO` são pensados para serem digitados/alterados ao vivo na gravação.
- Videoaulas puramente conceituais não têm pasta de código (ficam sem entrada nas tabelas acima, ou têm apenas um `README.md` com tópicos de fala).
- Python 3.12+ e Pydantic v2.
