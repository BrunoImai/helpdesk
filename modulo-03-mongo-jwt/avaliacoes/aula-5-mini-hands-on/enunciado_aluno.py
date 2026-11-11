"""
MINI HANDS-ON — Aula 5: escreva um teste que verifique o erro 401 Unauthorized de uma
rota protegida quando NENHUM token é enviado.

Execute:  pytest enunciado_aluno.py -v
"""

import os
import sys
from pathlib import Path

os.environ.setdefault("SECRET_KEY", "chave-somente-para-testes-0123456789abcdef")
os.environ.setdefault("MONGO_URI", "mongodb://banco-que-nunca-sera-usado:27017")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "projeto-final"))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

client = TestClient(app)


def test_listar_chamados_sem_token_devolve_401() -> None:
    # TODO 1: faça um GET em "/tickets" SEM o cabeçalho Authorization.
    # TODO 2: verifique que o status_code é 401.
    # TODO 3 (bônus): verifique o cabeçalho "www-authenticate".
    raise NotImplementedError
