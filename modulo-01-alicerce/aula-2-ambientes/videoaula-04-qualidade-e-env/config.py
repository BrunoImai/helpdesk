"""
VIDEOAULA 4 — Configurações lidas do ambiente (.env) com validação de tipos.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Valores com padrão: opcionais no .env
    app_name: str = "HelpDesk"
    debug: bool = False
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db_name: str = "helpdesk"

    # Sem padrão: OBRIGATÓRIA. Se faltar, o app nem inicia.
    secret_key: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
