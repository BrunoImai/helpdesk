# Videoaula 9 — Containers e Docker: instalação e comandos básicos (10 min)

**Objetivo:** entender o que é container e usar os comandos essenciais.
Não há código Python nesta aula; o "material" é este roteiro de comandos.

> **Nota:** o ambiente em que este material foi preparado **não tinha Docker instalado**. Os comandos abaixo
> são os padrões da ferramenta, mas rode todos antes de gravar.

## Conceitos
| Termo | Analogia | Definição |
|---|---|---|
| **Imagem** | Receita / "molde" | Pacote imutável com sistema + Python + dependências + código |
| **Container** | O prato pronto | Uma imagem **em execução**, isolada |
| **Dockerfile** | A receita escrita | Instruções para construir uma imagem |
| **Volume** | Armário fora da cozinha | Pasta que sobrevive ao container (dados do banco) |
| **Registry** (Docker Hub) | Loja de receitas | Onde imagens são publicadas/baixadas |

**Container x máquina virtual:** o container **compartilha o kernel** do sistema; é leve (MB, segundos).
A VM traz um sistema operacional inteiro (GB, minutos).

## Instalação (Windows)
1. Instale o **Docker Desktop** (<https://www.docker.com/products/docker-desktop/>). Requer WSL 2 (o instalador guia).
2. Reinicie, abra o Docker Desktop e aguarde "Engine running".
3. Teste:
```powershell
docker --version
docker run hello-world
```

## Comandos essenciais
```powershell
# --- Imagens ---
docker pull python:3.12-slim          # baixa uma imagem
docker images                         # lista imagens locais
docker rmi python:3.12-slim           # remove imagem

# --- Containers ---
docker run python:3.12-slim python -c "print('Olá de dentro do container!')"
docker run -it --rm python:3.12-slim bash       # shell interativo (--rm apaga ao sair)
docker run -d --name meu-mongo -p 27017:27017 mongo:7   # em segundo plano, expondo porta
docker ps                             # containers rodando
docker ps -a                          # todos (inclusive parados)
docker logs -f meu-mongo              # logs ao vivo
docker exec -it meu-mongo mongosh     # abre um comando DENTRO do container rodando
docker stop meu-mongo                 # para
docker rm meu-mongo                   # remove

# --- Limpeza ---
docker system prune                   # apaga containers parados/imagens sem uso (pede confirmação)
```

### Flags para memorizar
| Flag | Significado |
|---|---|
| `-d` | detached (segundo plano) |
| `-p 8000:8000` | mapeia **porta-do-host:porta-do-container** |
| `-e CHAVE=valor` / `--env-file .env` | variáveis de ambiente |
| `-v volume:/pasta` | monta volume |
| `--name` | dá um nome ao container |
| `--rm` | remove o container ao terminar |
| `-it` | interativo com terminal |

## Roteiro de gravação
1. "Funciona na minha máquina": o problema que o Docker resolve.
2. Imagem x container (analogia da receita) e container x VM.
3. Instalar e rodar `hello-world`.
4. `docker run` com Python; `-it` com bash (mostrar que o sistema lá dentro é outro).
5. Subir um Mongo com `-d -p`, olhar `docker ps`, `logs`, `exec`, `stop`, `rm`.
6. Gancho: "agora vamos criar a **nossa** imagem" (Videoaula 10).
