from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_DATABASE_URL = (
    "postgresql+psycopg://postgres:postgres@localhost:5433/noor_foods"
)


class Settings(BaseSettings):
    database_url: str = DEFAULT_DATABASE_URL

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
