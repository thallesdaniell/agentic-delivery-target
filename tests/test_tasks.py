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


@pytest.fixture
def mixed_client(client: TestClient) -> TestClient:
    client.post("/tasks", json={"title": "pendente"})
    client.post("/tasks", json={"title": "concluída"})
    client.post("/tasks/2/done")
    return client


def test_filters_done_tasks(mixed_client: TestClient) -> None:
    tasks = mixed_client.get("/tasks", params={"done": "true"}).json()

    assert [t["id"] for t in tasks] == [2]


def test_filters_pending_tasks(mixed_client: TestClient) -> None:
    tasks = mixed_client.get("/tasks", params={"done": "false"}).json()

    assert [t["id"] for t in tasks] == [1]


def test_lists_all_tasks_without_filter(mixed_client: TestClient) -> None:
    tasks = mixed_client.get("/tasks").json()

    assert [t["id"] for t in tasks] == [1, 2]


def test_deletes_a_task(client: TestClient) -> None:
    client.post("/tasks", json={"title": "apagar"})

    response = client.delete("/tasks/1")

    assert response.status_code == 204
    assert response.content == b""


def test_delete_unknown_task_returns_404(client: TestClient) -> None:
    assert client.delete("/tasks/999").status_code == 404


def test_deleted_task_is_gone(client: TestClient) -> None:
    client.post("/tasks", json={"title": "apagar"})
    client.delete("/tasks/1")

    assert client.get("/tasks/1").status_code == 404
    assert client.get("/tasks").json() == []


def test_renames_a_task_keeping_done(client: TestClient) -> None:
    client.post("/tasks", json={"title": "antigo"})
    client.post("/tasks/1/done")

    response = client.patch("/tasks/1", json={"title": "novo"})

    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "novo", "done": True}
    assert client.get("/tasks/1").json()["title"] == "novo"


def test_rename_missing_task_returns_404(client: TestClient) -> None:
    assert client.patch("/tasks/99", json={"title": "x"}).status_code == 404


def test_rename_rejects_empty_title(client: TestClient) -> None:
    client.post("/tasks", json={"title": "antigo"})

    assert client.patch("/tasks/1", json={"title": ""}).status_code == 422


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
