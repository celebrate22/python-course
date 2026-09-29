"""In-memory Tasks CRUD API.

Run:
    pip install fastapi uvicorn
    uvicorn main:app --reload

Docs: http://127.0.0.1:8000/docs
"""
from datetime import datetime, timezone
from itertools import count
from threading import Lock

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field

app = FastAPI(title="Tasks API")


class TaskIn(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    done: bool = False


class Task(TaskIn):
    id: int
    created_at: datetime



_tasks: dict[int, Task] = {}
_ids = count(1)
_lock = Lock()


def _get_or_404(task_id: int) -> Task:
    task = _tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.get("/tasks", response_model=list[Task])
def list_tasks():
    return list(_tasks.values())


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskIn):
    with _lock:
        task_id = next(_ids)
        task = Task(id=task_id, created_at=datetime.now(timezone.utc), **payload.model_dump())
        _tasks[task_id] = task
    return task


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    return _get_or_404(task_id)


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, payload: TaskIn):
    with _lock:
        existing = _get_or_404(task_id)
        updated = existing.model_copy(update=payload.model_dump())
        _tasks[task_id] = updated
    return updated


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    with _lock:
        _get_or_404(task_id)
        del _tasks[task_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)

