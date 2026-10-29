"""Configurações da aplicação, lidas das variáveis de ambiente / arquivo .env."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "HelpDesk API"
    debug: bool = False

    # MongoDB (local ou Atlas): ex. mongodb+srv://usuario:senha@cluster.mongodb.net
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db_name: str = "helpdesk"

    # JWT: SEM valor padrão de propósito. Sem SECRET_KEY o app não inicia.
    secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
