from fastapi.testclient import TestClient

from app.api.deps import get_llm
from app.main import create_app
from tests.conftest import FailingLLMProvider


def test_valid_request_returns_answer_and_key_points(client: TestClient) -> None:
    response = client.post(
        "/api/v1/interview/answer",
        json={"question": "Tell me about yourself", "role": "Flutter Developer"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body == {
        "answer": "I am a Flutter developer focused on clean architecture.",
        "key_points": ["Clean architecture", "Dart and Flutter"],
    }
    assert "model" not in body
    assert "test-key" not in response.text
    assert "GEMINI_API_KEY" not in response.text


def test_empty_question_returns_422(client: TestClient) -> None:
    response = client.post(
        "/api/v1/interview/answer",
        json={"question": "", "role": "Flutter Developer"},
    )

    assert response.status_code == 422


def test_gemini_service_failure_returns_502() -> None:
    app = create_app()
    app.dependency_overrides[get_llm] = lambda: FailingLLMProvider()
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/interview/answer",
            json={"question": "Tell me about yourself", "role": "Flutter Developer"},
        )

    assert response.status_code == 502
    assert "detail" in response.json()
    assert "test-key" not in response.text
