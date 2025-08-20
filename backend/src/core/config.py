"""
Configuration settings for the application
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # Security
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Database
    database_url: str = "sqlite:///./scholarmind.db"

    class Config:
        env_file = ".env"


settings = Settings()
