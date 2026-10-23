from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_", extra="ignore")

    name: str = "Implicit Volumes API"
    environment: str = "development"
    log_level: str = "INFO"
    log_json: bool = True

    database_url: str
    test_database_url: str | None = None
    database_echo: bool = False

    secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


@lru_cache
def get_settings() -> Settings:
    return Settings()
