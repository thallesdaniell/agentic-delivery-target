import pytest
from fastapi.testclient import TestClient

from tasks_api.app import create_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app())


def test_starts_empty(client: TestClient) -> None:
    assert client.get("/tasks").json() == []


def test_creates_and_reads_a_task(client: TestClient) -> None:
    created = client.post("/tasks", json={"title": "escrever o roadmap"})

    assert created.status_code == 201
    assert created.json() == {"id": 1, "title": "escrever o roadmap", "done": False}
    assert client.get("/tasks/1").json() == created.json()


def test_rejects_empty_title(client: TestClient) -> None:
    assert client.post("/tasks", json={"title": ""}).status_code == 422


def test_completes_a_task(client: TestClient) -> None:
    client.post("/tasks", json={"title": "abrir o PR"})

    done = client.post("/tasks/1/done")

    assert done.status_code == 200
    assert done.json()["done"] is True


def test_unknown_task_returns_404(client: TestClient) -> None:
    assert client.get("/tasks/99").status_code == 404
    assert client.post("/tasks/99/done").status_code == 404
