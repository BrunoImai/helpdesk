"""
VIDEOAULA 7 — Aplicação WSGI "crua" (síncrona), só com a biblioteca padrão.

Execute:  python app_wsgi.py   e abra http://127.0.0.1:8001/
"""

import json
from collections.abc import Callable, Iterable
from typing import Any
from wsgiref.simple_server import make_server


def application(
    environ: dict[str, Any], start_response: Callable[..., Any]
) -> Iterable[bytes]:
    """Interface WSGI: recebe o ambiente da requisição e uma função para iniciar a resposta."""
    caminho = environ["PATH_INFO"]
    corpo = json.dumps({"servidor": "WSGI", "caminho": caminho}).encode("utf-8")

    start_response(
        "200 OK",
        [("Content-Type", "application/json"), ("Content-Length", str(len(corpo)))],
    )
    return [corpo]


if __name__ == "__main__":
    with make_server("127.0.0.1", 8001, application) as servidor:
        print("WSGI em http://127.0.0.1:8001  (Ctrl+C para parar)")
        servidor.serve_forever()
