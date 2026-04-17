from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    # Server
    APP_NAME: str = "Production AI Agent"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    PORT: int = int(os.getenv("PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Security
    AGENT_API_KEY: str = os.getenv("AGENT_API_KEY", "default-secret-key")
    
    # Rate Limiting & Budget
    RATE_LIMIT_PER_MINUTE: int = 10
    MONTHLY_BUDGET_USD: float = 10.0
    COST_PER_REQUEST: float = 0.01  # Giả định mỗi request tốn $0.01

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
