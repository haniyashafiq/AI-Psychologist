"""OpenAI embedding service for generating text embeddings"""
from openai import AsyncOpenAI
from typing import List
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config.settings import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class EmbeddingService:
    """Generates text embeddings using OpenAI's embedding API"""

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.embedding_model
        self.dimensions = settings.embedding_dimensions

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
    )
    async def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text string"""
        response = await self.client.embeddings.create(
            model=self.model,
            input=text,
            dimensions=self.dimensions,
        )
        return response.data[0].embedding

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
    )
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a batch of texts"""
        response = await self.client.embeddings.create(
            model=self.model,
            input=texts,
            dimensions=self.dimensions,
        )
        return [item.embedding for item in response.data]

    def embed_text_sync(self, text: str) -> List[float]:
        """Synchronous embedding for use in ingestion scripts"""
        from openai import OpenAI

        client = OpenAI(api_key=settings.openai_api_key)
        response = client.embeddings.create(
            model=self.model,
            input=text,
            dimensions=self.dimensions,
        )
        return response.data[0].embedding

    def embed_batch_sync(self, texts: List[str]) -> List[List[float]]:
        """Synchronous batch embedding for use in ingestion scripts"""
        from openai import OpenAI

        client = OpenAI(api_key=settings.openai_api_key)
        response = client.embeddings.create(
            model=self.model,
            input=texts,
            dimensions=self.dimensions,
        )
        return [item.embedding for item in response.data]
