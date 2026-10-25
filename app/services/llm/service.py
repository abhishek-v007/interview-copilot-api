import json
import logging
import re

from pydantic import BaseModel, Field, ValidationError

from app.services.llm.base import LLMAnswer, LLMProvider, LLMResult

logger = logging.getLogger(__name__)

_FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE)


class _ParsedAnswer(BaseModel):
    answer: str
    key_points: list[str] = Field(default_factory=list)


class LLMService:
    """Dedicated LLM service used by InterviewService.

    Wraps a provider (Gemini in Phase 1) and normalizes structured output.
    HTTP routes never call this around the Gemini SDK directly.
    """

    def __init__(self, provider: LLMProvider) -> None:
        self._provider = provider

    async def generate(self, prompt: str) -> LLMAnswer:
        result: LLMResult = await self._provider.generate(prompt)
        return self._parse(result.text)

    @staticmethod
    def _parse(text: str) -> LLMAnswer:
        stripped = _FENCE_RE.sub("", text.strip()).strip()
        try:
            parsed = _ParsedAnswer.model_validate(json.loads(stripped))
        except (json.JSONDecodeError, ValidationError, TypeError):
            logger.info("LLM response was not structured JSON; using raw text")
            return LLMAnswer(answer=stripped, key_points=[])
        return LLMAnswer(answer=parsed.answer, key_points=parsed.key_points)
