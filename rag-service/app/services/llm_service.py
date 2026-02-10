"""OpenAI LLM service for clinical assessment generation"""
import json
from openai import AsyncOpenAI
from typing import Dict, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
import tiktoken

from app.config.settings import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class LLMService:
    """Handles OpenAI chat completion calls with structured output"""

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.max_tokens = settings.max_completion_tokens
        self.temperature = settings.temperature
        self._encoder = None

    @property
    def encoder(self):
        """Lazy-load tiktoken encoder"""
        if self._encoder is None:
            try:
                self._encoder = tiktoken.encoding_for_model(self.model)
            except KeyError:
                self._encoder = tiktoken.get_encoding("cl100k_base")
        return self._encoder

    def count_tokens(self, text: str) -> int:
        """Count tokens in a text string"""
        return len(self.encoder.encode(text))

    def truncate_to_token_limit(self, text: str, max_tokens: int) -> str:
        """Truncate text to fit within a token limit"""
        tokens = self.encoder.encode(text)
        if len(tokens) <= max_tokens:
            return text
        truncated_tokens = tokens[:max_tokens]
        return self.encoder.decode(truncated_tokens)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=15),
    )
    async def generate_assessment(
        self,
        system_prompt: str,
        user_prompt: str,
        response_format: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Generate a clinical assessment using the LLM.
        Returns parsed JSON response.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        # Log token usage estimate
        total_input = system_prompt + user_prompt
        input_tokens = self.count_tokens(total_input)
        logger.info(
            f"LLM call: model={self.model}, input_tokens≈{input_tokens}, "
            f"max_output={self.max_tokens}"
        )

        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "response_format": {"type": "json_object"},
        }

        response = await self.client.chat.completions.create(**kwargs)

        content = response.choices[0].message.content
        usage = response.usage

        logger.info(
            f"LLM response: prompt_tokens={usage.prompt_tokens}, "
            f"completion_tokens={usage.completion_tokens}, "
            f"total_tokens={usage.total_tokens}"
        )

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM JSON response: {e}")
            logger.error(f"Raw content: {content[:500]}")
            parsed = {
                "clinical_narrative": content,
                "parse_error": True,
            }

        return {
            "result": parsed,
            "usage": {
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens,
                "model": self.model,
            },
        }
