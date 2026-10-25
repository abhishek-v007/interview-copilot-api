import pytest

from app.core.config import Settings
from app.core.exceptions import LLMProviderError
from app.services.llm.base import LLMResult
from app.services.llm.factory import get_llm_provider
from app.services.llm.gemini import GeminiProvider
from app.services.llm.service import LLMService


class _StaticProvider:
    def __init__(self, text: str) -> None:
        self._text = text

    async def generate(self, prompt: str) -> LLMResult:
        return LLMResult(text=self._text, model="fake-model")


class _FailingProvider:
    async def generate(self, prompt: str) -> LLMResult:
        raise LLMProviderError("provider unavailable")


def test_factory_returns_gemini_provider() -> None:
    settings = Settings(
        app_env="development",
        gemini_api_key="test-key",
        gemini_model="gemini-2.0-flash",
    )

    provider = get_llm_provider(settings)

    assert isinstance(provider, GeminiProvider)
    assert provider.model == "gemini-2.0-flash"


def test_factory_requires_api_key_outside_test() -> None:
    settings = Settings(app_env="development", gemini_api_key="")

    with pytest.raises(RuntimeError, match="GEMINI_API_KEY"):
        get_llm_provider(settings)


@pytest.mark.asyncio
async def test_llm_service_parses_structured_json() -> None:
    service = LLMService(
        _StaticProvider(
            '{"answer": "A spoken answer.", "key_points": ["Point A", "Point B"]}'
        )
    )

    result = await service.generate("prompt")

    assert result.answer == "A spoken answer."
    assert result.key_points == ["Point A", "Point B"]


@pytest.mark.asyncio
async def test_llm_service_propagates_provider_failure() -> None:
    service = LLMService(_FailingProvider())

    with pytest.raises(LLMProviderError):
        await service.generate("prompt")
