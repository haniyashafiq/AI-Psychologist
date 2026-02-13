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
        """Synchronous batch embedding for use in ingestion scripts.
        Handles token limits by truncating long texts and splitting into sub-batches."""
        import tiktoken
        from openai import OpenAI

        client = OpenAI(api_key=settings.openai_api_key)

        # Get encoder for token counting / truncation
        try:
            encoder = tiktoken.encoding_for_model(self.model)
        except KeyError:
            encoder = tiktoken.get_encoding("cl100k_base")

        max_tokens_per_text = 8000  # Leave margin below 8191 limit

        # Truncate any texts that exceed the token limit
        safe_texts = []
        for text in texts:
            tokens = encoder.encode(text)
            if len(tokens) > max_tokens_per_text:
                safe_texts.append(encoder.decode(tokens[:max_tokens_per_text]))
            else:
                safe_texts.append(text)

        # Process in sub-batches to avoid total token limits
        all_embeddings = []
        sub_batch_size = 20  # Smaller batches to stay within API limits
        for i in range(0, len(safe_texts), sub_batch_size):
            sub_batch = safe_texts[i:i + sub_batch_size]
            response = client.embeddings.create(
                model=self.model,
                input=sub_batch,
                dimensions=self.dimensions,
            )
            all_embeddings.extend([item.embedding for item in response.data])

        return all_embeddings
