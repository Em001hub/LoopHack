from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "ProjectMind Integration Service"
    DATABASE_URL: str = "postgresql://user:password@db:5432/projectmind"
    REDIS_URL: str = "redis://redis:6379/0"
    
    # Integration Credentials
    JIRA_DOMAIN: Optional[str] = None
    JIRA_EMAIL: Optional[str] = None
    JIRA_API_TOKEN: Optional[str] = None
    
    GITHUB_TOKEN: Optional[str] = None
    SLACK_TOKEN: Optional[str] = None
    GOOGLE_ACCESS_TOKEN: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()
