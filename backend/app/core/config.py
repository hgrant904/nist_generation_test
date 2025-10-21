from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic.functional_validators import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = Field(default="NIST Reports API", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    log_level: str = Field(default="info", alias="LOG_LEVEL")
    database_url: str = Field(default="sqlite+aiosqlite:///./app.db", alias="DATABASE_URL")
    sync_database_url: str | None = Field(default=None, alias="SYNC_DATABASE_URL")
    llm_provider: str = Field(default="ollama", alias="LLM_PROVIDER")
    ollama_base_url: str = Field(default="http://host.docker.internal:11434", alias="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="llama3.1:8b", alias="OLLAMA_MODEL")
    ollama_temperature: float = Field(default=0.2, alias="OLLAMA_TEMPERATURE")
    ollama_num_predict: int = Field(default=256, alias="OLLAMA_NUM_PREDICT")
    allowed_origins: List[str] = Field(
        default_factory=lambda: ["http://localhost:3000"], alias="ALLOWED_ORIGINS"
    )

    model_config = SettingsConfigDict(
        env_file=("backend/.env", ".env"),
        env_file_encoding="utf-8",
        extra="allow",
    )

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return ["http://localhost:3000"]

    def get_sync_database_url(self) -> str:
        """Return a synchronous SQLAlchemy connection string for tooling such as Alembic."""

        if self.sync_database_url:
            return self.sync_database_url

        url = make_url(self.database_url)
        driver = url.drivername

        if driver.endswith("+asyncpg"):
            sync_driver = driver.replace("+asyncpg", "+psycopg")
        elif driver.endswith("+aiosqlite"):
            sync_driver = driver.replace("+aiosqlite", "")
        else:
            sync_driver = driver

        sync_url = url.set(drivername=sync_driver)
        return sync_url.render_as_string(hide_password=False)


@lru_cache()
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()
