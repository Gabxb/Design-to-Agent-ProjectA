from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_health_returns_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task_requires_content() -> None:
    response = client.post("/tasks", json={"title": "Example", "content": "A safe synthetic example."})
    assert response.status_code == 201
    assert response.json()["state"] == "pending_approval"
