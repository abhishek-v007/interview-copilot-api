import asyncio
import logging

from google import genai
from google.genai import types

from app.core.exceptions import LLMProviderError, LLMTimeoutError
from app.services.llm.base import LLMResult

logger = logging.getLogger(__name__)


class GeminiProvider:
    """Gemini implementation of LLMProvider. Used only by LLMService."""

    def __init__(self, api_key: str, model: str, timeout_seconds: float) -> None:
        self.model = model
        self._timeout_seconds = timeout_seconds
        self._client = genai.Client(api_key=api_key)

    async def generate(self, prompt: str) -> LLMResult:
        try:
            response = await asyncio.wait_for(
                self._client.aio.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                    ),
                ),
                timeout=self._timeout_seconds,
            )
        except TimeoutError as exc:
            logger.warning("Gemini request timed out model=%s", self.model)
            raise LLMTimeoutError() from exc
        except LLMProviderError:
            raise
        except Exception as exc:
            logger.exception("Gemini request failed model=%s", self.model)
            raise LLMProviderError() from exc

        text = (getattr(response, "text", None) or "").strip()
        if not text:
            raise LLMProviderError("The language model returned an empty answer.")

        return LLMResult(text=text, model=self.model)
