"""VIDEOAULA 9 — Configurações (agora com os parâmetros do JWT)."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db_name: str = "helpdesk"

    # Sem valor padrão: se faltar no .env, a API não inicia (melhor que usar uma chave fraca)
    secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
