"""Armazenamento de tarefas em memória."""

from pydantic import BaseModel


class Task(BaseModel):
    id: int
    title: str
    done: bool = False


class TaskStore:
    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id = 1

    def list(self) -> list[Task]:
        return list(self._tasks.values())

    def add(self, title: str) -> Task:
        task = Task(id=self._next_id, title=title)
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Task | None:
        return self._tasks.get(task_id)

    def complete(self, task_id: int) -> Task | None:
        task = self._tasks.get(task_id)
        if task is None:
            return None
        task.done = True
        return task

    def delete(self, task_id: int) -> bool:
        return self._tasks.pop(task_id, None) is not None
