import os
from dataclasses import dataclass


@dataclass
class Settings:
    app_name: str = os.getenv("APP_NAME", "NIST Reports API")
    app_description: str = os.getenv(
        "APP_DESCRIPTION", "API for automating NIST security report generation"
    )
    app_version: str = os.getenv("APP_VERSION", "0.1.0")

    allowed_origins: list[str] = None  # set in __post_init__

    # Database
    postgres_user: str = os.getenv("POSTGRES_USER", "postgres")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    postgres_db: str = os.getenv("POSTGRES_DB", "nist")
    postgres_host: str = os.getenv("POSTGRES_HOST", "db")
    postgres_port: str = os.getenv("POSTGRES_PORT", "5432")

    # Ollama
    ollama_host: str = os.getenv("OLLAMA_HOST", "http://localhost")
    ollama_port: str = os.getenv("OLLAMA_PORT", "11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

    def __post_init__(self):
        allowed = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
        self.allowed_origins = [o.strip() for o in allowed.split(",") if o.strip()]

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


def get_settings() -> Settings:
    return Settings()
