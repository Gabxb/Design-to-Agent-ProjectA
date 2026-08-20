from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_env: str = "dev"
    database_url: str = "sqlite:///./agent.db"
    openai_api_key: str = ""
    openai_model: str = "gpt-5-mini"
    model_timeout_s: float = 30.0
    max_agent_steps: int = 8
@lru_cache
def get_settings() -> Settings: return Settings()
