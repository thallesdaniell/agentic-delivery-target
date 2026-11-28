"""API HTTP de tarefas, com armazenamento em memória."""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from tasks_api.store import Task, TaskStore


class NewTask(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=200)


def create_app(store: TaskStore | None = None) -> FastAPI:
    store = store or TaskStore()
    app = FastAPI(title="tasks-api")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/tasks")
    def list_tasks(done: bool | None = None, q: str | None = None) -> list[Task]:
        tasks = store.list()
        if done is not None:
            tasks = [task for task in tasks if task.done == done]
        if q:
            needle = q.casefold()
            tasks = [task for task in tasks if needle in task.title.casefold()]
        return tasks

    @app.post("/tasks", status_code=status.HTTP_201_CREATED)
    def create_task(body: NewTask) -> Task:
        return store.add(body.title)

    @app.get("/tasks/stats")
    def task_stats() -> dict[str, int]:
        tasks = store.list()
        done = sum(1 for task in tasks if task.done)
        return {"total": len(tasks), "done": done, "pending": len(tasks) - done}

    @app.get("/tasks/{task_id}")
    def get_task(task_id: int) -> Task:
        task = store.get(task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="task not found")
        return task

    @app.patch("/tasks/{task_id}")
    def rename_task(task_id: int, body: NewTask) -> Task:
        task = store.get(task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="task not found")
        task.title = body.title
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
