"""
Configuration settings for Intelligence Service
"""

from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Service
    SERVICE_NAME: str = "intelligence-service"
    SERVICE_PORT: int = 4002
    LOG_LEVEL: str = "INFO"
    
    # Database
    DATABASE_URL: str = "postgresql://admin:password@localhost:5432/projectmind"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    
    # Anthropic
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # ML Configuration
    ML_MODEL_PATH: str = "./src/data/models"
    ENABLE_GPU: bool = False
    BATCH_SIZE: int = 32
    
    # Feature Flags
    ENABLE_SKILL_EXTRACTION: bool = True
    ENABLE_TIMELINE_PREDICTION: bool = True
    ENABLE_SENTIMENT_ANALYSIS: bool = True
    ENABLE_CONVERSATION_INTELLIGENCE: bool = True
    
    # Performance
    MAX_WORKERS: int = 4
    PREDICTION_CACHE_TTL: int = 3600
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
