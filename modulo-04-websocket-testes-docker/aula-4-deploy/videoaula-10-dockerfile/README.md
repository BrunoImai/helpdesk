# Videoaula 10 — Criando o Dockerfile da API (12 min)

**Objetivo:** empacotar a API do HelpDesk em uma imagem.

**Arquivos:** [`Dockerfile`](Dockerfile) e [`.dockerignore`](.dockerignore) (cópias de `projeto-final/`, que é de
onde você roda o build — o `Dockerfile` precisa estar na mesma pasta de `requirements.txt`, `app/` e `scripts/`).

> O ambiente de preparação **não tinha Docker**: o Dockerfile foi escrito conforme a documentação, mas rode o
> `docker build` antes de gravar.

## Como rodar
```powershell
cd ..\..\projeto-final
docker build -t helpdesk-api .
docker run --rm -p 8000:8000 `
  -e SECRET_KEY=troque-esta-chave `
  -e MONGO_URI=mongodb://host.docker.internal:27017 `
  helpdesk-api
```
(`host.docker.internal` = o Mongo que roda na sua máquina, fora do container. Na Videoaula 11 o Compose resolve isso.)

## Instrução por instrução
| Instrução | Por quê |
|---|---|
| `FROM python:3.12-slim` | Base enxuta (muito menor que a imagem completa) |
| `ENV PYTHONUNBUFFERED=1 ...` | Logs na hora; sem `.pyc`; pip sem cache (imagem menor) |
| `WORKDIR /app` | Pasta de trabalho dentro do container |
| `COPY requirements.txt .` + `RUN pip install` **antes** do código | **Cache de camadas:** se só o código muda, as dependências não são reinstaladas |
| `COPY app ./app` | Só o que a API precisa (o resto é filtrado pelo `.dockerignore`) |
| `RUN useradd ... / USER appuser` | **Não rodar como root** (segurança) |
| `EXPOSE 8000` | Documenta a porta (quem publica de fato é o `-p`) |
| `HEALTHCHECK` | O Docker sabe se a API está viva (`docker ps` mostra `healthy`) |
| `CMD ["uvicorn", ... "--host", "0.0.0.0"]` | `0.0.0.0` é obrigatório: `127.0.0.1` dentro do container não é alcançável de fora |

## `.dockerignore`
Evita enviar para o build: `.env` (segredos!), `.venv`, `tests/`, caches e `.git`. Resultado: build mais rápido,
imagem menor e **sem vazar senhas**.

## Roteiro de gravação
1. Mostrar o Dockerfile vazio e construir linha a linha.
2. Rodar `docker build` duas vezes: na 2ª, tudo vem do cache. Mudar um arquivo em `app/` e ver só as últimas camadas refeitas.
3. `docker run` e abrir `/docs`. A API sobe, mas falha ao conectar no Mongo (sem banco) -> gancho para o Compose.
4. Erros comuns: esquecer `0.0.0.0`; copiar `.env` para a imagem.
