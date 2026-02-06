"""Application settings and configuration"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "info"
    spacy_model: str = "en_core_web_md"
    max_text_length: int = 5000
    enable_cors: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
