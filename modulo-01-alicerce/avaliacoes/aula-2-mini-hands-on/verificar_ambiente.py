"""
AVALIAÇÃO DA AULA 2 — Verificador do mini hands-on.

Rode DENTRO da pasta do projeto do aluno, com o ambiente virtual ativo:
    python verificar_ambiente.py
"""

import sys
from importlib import metadata
from pathlib import Path


def ler_env(caminho: Path) -> dict[str, str]:
    valores: dict[str, str] = {}
    for linha in caminho.read_text(encoding="utf-8-sig").splitlines():
        linha = linha.strip()
        if linha and not linha.startswith("#") and "=" in linha:
            chave, _, valor = linha.partition("=")
            valores[chave.strip()] = valor.strip()
    return valores


def verificar() -> list[tuple[str, bool]]:
    resultados: list[tuple[str, bool]] = []

    resultados.append(("Ambiente virtual ativo", sys.prefix != sys.base_prefix))

    try:
        metadata.version("fastapi")
        fastapi_ok = True
    except metadata.PackageNotFoundError:
        fastapi_ok = False
    resultados.append(("FastAPI instalado", fastapi_ok))

    env = Path(".env")
    chave_ok = env.exists() and len(ler_env(env).get("SECRET_KEY", "")) >= 32
    resultados.append((".env com SECRET_KEY (>= 32 caracteres)", chave_ok))

    gitignore = Path(".gitignore")
    ignorado = gitignore.exists() and ".env" in {
        linha.strip() for linha in gitignore.read_text(encoding="utf-8").splitlines()
    }
    resultados.append((".env listado no .gitignore", ignorado))

    return resultados


if __name__ == "__main__":
    resultados = verificar()
    for descricao, ok in resultados:
        print(f"[{'OK' if ok else 'FALHOU'}] {descricao}")
    aprovados = sum(ok for _, ok in resultados)
    print(f"\nResultado: {aprovados}/{len(resultados)} critérios atendidos")
    sys.exit(0 if aprovados == len(resultados) else 1)
