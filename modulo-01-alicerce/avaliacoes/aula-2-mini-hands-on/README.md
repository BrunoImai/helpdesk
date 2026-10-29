# Avaliação da Aula 2 — Mini Hands-on (gabarito)

**Desafio do aluno:** inicializar um ambiente virtual, instalar o FastAPI e criar um arquivo `.env` seguro.

## Passo a passo esperado (Windows PowerShell)
```powershell
mkdir helpdesk; cd helpdesk
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install fastapi
pip freeze > requirements.txt

# .env com segredo gerado (não escreva uma senha "na mão")
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))" > .env
echo "DEBUG=true" >> .env

# .gitignore protegendo o .env e o .venv
echo ".env" >> .gitignore
echo ".venv/" >> .gitignore
```

## Verificação automática
Execute na pasta do aluno, com o ambiente ativo:
```powershell
python ..\caminho\para\verificar_ambiente.py
```
O script [`verificar_ambiente.py`](verificar_ambiente.py) confere os 4 critérios abaixo.

## Critérios de correção
| # | Critério |
|---|---|
| 1 | Está executando dentro de um ambiente virtual |
| 2 | O pacote `fastapi` está instalado nesse ambiente |
| 3 | Existe um arquivo `.env` com `SECRET_KEY` de pelo menos 32 caracteres |
| 4 | O `.env` está listado no `.gitignore` (não será versionado) |
