"""Configuration settings for RAG service"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """RAG service configuration loaded from environment variables"""

    # Server
    host: str = "0.0.0.0"
    port: int = 8001
    log_level: str = "info"

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536
    max_completion_tokens: int = 4096
    temperature: float = 0.2

    # ChromaDB
    chroma_persist_dir: str = "/data/chroma_db"
    chroma_collection_name: str = "dsm5"

    # Retrieval
    retrieval_top_k: int = 8
    retrieval_min_score: float = 0.3

    # Ingestion
    chunk_size: int = 800
    chunk_overlap: int = 150

    # CORS
    enable_cors: bool = True

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
