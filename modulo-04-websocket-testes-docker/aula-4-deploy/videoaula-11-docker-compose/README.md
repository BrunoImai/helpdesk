# Videoaula 11 — Orquestrando API e MongoDB com Docker Compose (15 min)

**Objetivo:** subir o HelpDesk inteiro (API + banco) com **um** comando.

**Arquivo:** [`docker-compose.yml`](docker-compose.yml) (cópia de `projeto-final/docker-compose.yml`).

> O ambiente de preparação **não tinha Docker**: o YAML foi validado quanto à sintaxe, mas **rode
> `docker compose up --build` antes de gravar**. `docker compose config` também valida o arquivo.

## Como rodar
```powershell
cd ..\..\projeto-final
copy .env.example .env                  # preencha SECRET_KEY
docker compose up --build               # sobe tudo (Ctrl+C para parar)
docker compose exec api python -m scripts.criar_agente "Ana Souza" ana@helpdesk.com
```
Abra <http://127.0.0.1:8000/docs> e <http://127.0.0.1:8000/chat>.

## Imagem x Compose
| Dockerfile | docker-compose.yml |
|---|---|
| **Uma** imagem (a receita de um prato) | **Vários** serviços juntos (o cardápio completo) |
| `docker build` / `docker run` | `docker compose up` |
| Descreve *como construir* | Descreve *como executar e conectar* |

## Pontos-chave do arquivo
- **`services`**: `mongo` (imagem oficial) e `api` (construída do nosso Dockerfile).
- **Rede e DNS interno:** a API acessa o banco por `mongodb://mongo:27017`, onde `mongo` é o **nome do serviço**.
  Dentro do container, `localhost` seria o próprio container, e não o banco!
- **`depends_on` + `healthcheck`:** a API só inicia quando o Mongo responde ao ping (`service_healthy`).
- **`volumes: mongo_data`:** os dados sobrevivem a `docker compose down`. Só `down -v` apaga.
- **`ports`:** só a API é publicada (`8000:8000`). O Mongo fica **inacessível de fora** (mais seguro).
- **Segredos:** `SECRET_KEY: ${SECRET_KEY:?...}` vem do `.env`; o Compose se recusa a subir sem ela.

## Comandos úteis
```powershell
docker compose up -d --build     # segundo plano
docker compose ps                # estado e "healthy"
docker compose logs -f api       # logs da API
docker compose exec mongo mongosh  # entrar no banco
docker compose down              # derruba (mantém dados)
docker compose down -v           # derruba e apaga dados
```

## Roteiro de gravação
1. Dor: três terminais, três comandos, ordem certa... -> um arquivo só.
2. Construir o YAML: `mongo`, depois `api`; explicar o DNS por nome de serviço.
3. `up --build`; abrir `/docs`; criar o atendente; fazer login; abrir o chat em duas abas.
4. `down` e `up` de novo: os chamados continuam lá (volume). Depois `down -v` e mostrar que sumiram.
5. Fechamento do módulo: conectar com o **Projeto Final** (chat + testes + Docker).
