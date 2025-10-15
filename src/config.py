from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )
    
    llm_provider: str = "ollama"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"
    ollama_temperature: float = 0.7
    ollama_num_predict: int = 512
    
    database_url: str = "sqlite+aiosqlite:///./nist_csf.db"
    
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    
    log_level: str = "INFO"


settings = Settings()
