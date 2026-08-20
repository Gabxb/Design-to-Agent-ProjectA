"""Runtime configuration loaded from environment variables."""

from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings. Values are intentionally safe by default."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    log_level: str = "INFO"
    database_url: str = "sqlite:///./agent.db"
    model_base_url: str = "https://api.openai.com/v1"
    model_api_key: SecretStr = SecretStr("replace_me")
    model_name: str = "gpt-5-mini"
    model_timeout_seconds: float = Field(default=30.0, gt=0, le=120)
    request_timeout_seconds: float = Field(default=15.0, gt=0, le=60)
    max_agent_steps: int = Field(default=6, ge=1, le=12)
    max_tool_retries: int = Field(default=1, ge=0, le=3)
    enable_write_tools: bool = False


@lru_cache
def get_settings() -> Settings:
    """Return a process-wide immutable settings instance."""

    return Settings()
