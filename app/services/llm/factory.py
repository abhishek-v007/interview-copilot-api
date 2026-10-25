from app.core.config import Settings
from app.services.llm.base import LLMProvider
from app.services.llm.gemini import GeminiProvider


def get_llm_provider(settings: Settings) -> LLMProvider:
    """Build the configured LLM provider.

    Gemini is the Phase 1 implementation. A future provider is a new class
    plus a branch here — callers depend only on LLMProvider.
    """

    if not settings.is_test and not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is required when APP_ENV is not test. "
            "Copy .env.example to .env and set a real Gemini API key."
        )

    return GeminiProvider(
        api_key=settings.gemini_api_key,
        model=settings.gemini_model,
        timeout_seconds=settings.gemini_timeout_seconds,
    )
