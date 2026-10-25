import os

os.environ["APP_ENV"] = "test"
os.environ.setdefault("GEMINI_API_KEY", "test-key")
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+psycopg://user:password@localhost:5432/interview_copilot",
)

import pytest
from fastapi.testclient import TestClient

from app.api.deps import get_llm
from app.core.config import get_settings
from app.core.exceptions import LLMProviderError
from app.main import create_app
from app.services.llm.base import LLMResult

get_settings.cache_clear()


class FakeLLMProvider:
    async def generate(self, prompt: str) -> LLMResult:
        return LLMResult(
            text=(
                '{"answer": "I am a Flutter developer focused on clean architecture.",'
                ' "key_points": ["Clean architecture", "Dart and Flutter"]}'
            ),
            model="fake-model",
        )


class FailingLLMProvider:
    async def generate(self, prompt: str) -> LLMResult:
        raise LLMProviderError("provider unavailable")


@pytest.fixture
def fake_llm() -> FakeLLMProvider:
    return FakeLLMProvider()


@pytest.fixture
def client(fake_llm: FakeLLMProvider) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_llm] = lambda: fake_llm
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
