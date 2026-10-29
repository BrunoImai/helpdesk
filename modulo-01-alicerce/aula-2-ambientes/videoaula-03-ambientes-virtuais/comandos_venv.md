# VIDEOAULA 3 — `venv` + `pip`

## Windows (PowerShell)
```powershell
cd helpdesk
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
# Se der erro de política de execução:
#   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
python -m pip install --upgrade pip
pip install fastapi "uvicorn[standard]" "pydantic[email]" pydantic-settings
pip list
pip freeze > requirements.txt
deactivate
```

## Linux / macOS
```bash
cd helpdesk
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install fastapi "uvicorn[standard]" "pydantic[email]" pydantic-settings
pip freeze > requirements.txt
deactivate
```

## Reproduzindo em outra máquina
```bash
git clone https://github.com/<usuario>/helpdesk.git
cd helpdesk
python -m venv .venv
# ativar o ambiente (veja acima)
pip install -r requirements.txt
```

## Regras de ouro
- Um ambiente virtual **por projeto**.
- A pasta `.venv/` entra no `.gitignore`. O que se versiona é o `requirements.txt`.
- Sempre ative o ambiente antes de instalar pacotes (confira o prefixo `(.venv)` no terminal).
