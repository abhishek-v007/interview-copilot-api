from fastapi.testclient import TestClient


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "interview-copilot-api"}


def test_root_lists_available_routes(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "interview-copilot-api"
    assert body["health"] == "/health"
    assert body["docs"] == "/docs"
