from typing import Protocol

from pydantic import BaseModel, Field


class LLMResult(BaseModel):
    """Raw provider output. Not the HTTP response contract."""

    text: str
    model: str


class LLMAnswer(BaseModel):
    """Structured result returned by LLMService to InterviewService."""

    answer: str
    key_points: list[str] = Field(default_factory=list)


class LLMProvider(Protocol):
    """Replaceable language-model client used by LLMService."""

    async def generate(self, prompt: str) -> LLMResult: ...
