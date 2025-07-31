import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    app_name: str = "ScholarMind API"
    debug: bool = False
    version: str = "1.0.0"
    
    # Database
    database_url: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://scholarmind_user:scholarmind_pass@localhost:5432/scholarmind_db"
    )
    
    # Vector Database
    vector_db_url: str = os.getenv("VECTOR_DB_URL", "http://localhost:8001")
    chroma_host: str = os.getenv("CHROMA_HOST", "localhost")
    chroma_port: int = int(os.getenv("CHROMA_PORT", "8001"))
    
    # OpenAI API
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # LangSmith (optional for LangChain tracing)
    langsmith_api_key: Optional[str] = os.getenv("LANGSMITH_API_KEY")
    langsmith_project: str = os.getenv("LANGSMITH_PROJECT", "scholarmind")
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # File upload
    max_file_size: int = 50 * 1024 * 1024  # 50MB
    upload_dir: str = os.getenv("UPLOAD_DIR", "/tmp/uploads")
    
    # CORS
    allowed_origins: list = ["http://localhost:3000", "http://localhost:3001"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
