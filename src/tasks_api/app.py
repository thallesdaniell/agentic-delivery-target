"""API HTTP de tarefas, com armazenamento em memória."""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from tasks_api.store import Task, TaskStore


class NewTask(BaseModel):
    title: str = Field(min_length=1, max_length=200)


def create_app(store: TaskStore | None = None) -> FastAPI:
    store = store or TaskStore()
    app = FastAPI(title="tasks-api")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/tasks")
    def list_tasks() -> list[Task]:
        return store.list()

    @app.post("/tasks", status_code=status.HTTP_201_CREATED)
    def create_task(body: NewTask) -> Task:
        return store.add(body.title)

    @app.get("/tasks/{task_id}")
    def get_task(task_id: int) -> Task:
        task = store.get(task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="task not found")
        return task

    @app.post("/tasks/{task_id}/done")
    def complete_task(task_id: int) -> Task:
        task = store.complete(task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="task not found")
        return task

    @app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_task(task_id: int) -> None:
        if not store.delete(task_id):
            raise HTTPException(status_code=404, detail="task not found")

    return app


app = create_app()
