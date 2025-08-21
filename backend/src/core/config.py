"""
Configuration settings for the application
"""

import logging

from pydantic_settings import BaseSettings

# Configure logger for this module
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings"""

    # Security - These MUST be set via environment variables
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    environment: str = "development"

    # Database
    database_url: str = "sqlite:///./scholarmind.db"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Validate secret key strength
        if len(self.secret_key) < 32:
            raise ValueError(
                f"SECRET_KEY must be at least 32 characters long. "
                f"Current length: {len(self.secret_key)}"
            )

        # Warn about default/weak keys
        weak_keys = [
            "your-secret-key-change-in-production",
            "your-super-secret-key-change-in-production-please",
            "secret",
            "development",
            "test",
            "password",
        ]

        if self.secret_key in weak_keys:
            if self.environment == "production":
                raise ValueError(
                    "Using a default or weak SECRET_KEY in production is not allowed!"
                )
            else:
                logger.warning(
                    "Using a weak SECRET_KEY. Generate a secure one for production!"
                )

    class Config:
        env_file = ".env"
        case_sensitive = False  # Allow lowercase env variables


settings = Settings()
