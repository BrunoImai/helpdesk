# ============================================================================
# HelpDesk API — imagem Docker
# Build:  docker build -t helpdesk-api .
# Run:    docker run --rm -p 8000:8000 --env-file .env helpdesk-api
# ============================================================================

# 1. Imagem base: Python enxuto (bem menor que a "python:3.12" completa)
FROM python:3.12-slim

# 2. Variáveis de ambiente do Python dentro do container
#    - não gerar .pyc; mostrar logs na hora (sem buffer); pip sem cache
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# 3. Pasta de trabalho dentro do container
WORKDIR /app

# 4. Instala as dependências ANTES de copiar o código.
#    Assim o Docker reaproveita esta camada (cache) enquanto o requirements.txt não mudar.
COPY requirements.txt .
RUN pip install -r requirements.txt

# 5. Copia o código da aplicação
COPY app ./app
COPY scripts ./scripts

# 6. Segurança: roda com um usuário comum, NÃO como root
RUN useradd --create-home --uid 1000 appuser
USER appuser

# 7. Documenta a porta usada pela API
EXPOSE 8000

# 8. O Docker verifica periodicamente se a API continua respondendo
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/', timeout=3)" || exit 1

# 9. Comando que inicia a API (0.0.0.0 = aceita conexões de fora do container)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
