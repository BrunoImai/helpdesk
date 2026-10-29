"""Configurações da aplicação, lidas das variáveis de ambiente / arquivo .env."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "HelpDesk API"
    debug: bool = False
    secret_key: str = "inseguro-apenas-para-desenvolvimento"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
