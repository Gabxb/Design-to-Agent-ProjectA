"""Teaching-only API skeleton for 案例分流与合规助手."""
from __future__ import annotations

import logging
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
app = FastAPI(title="案例分流与合规助手", version="0.1.0")


class TaskRequest(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    content: str = Field(min_length=1, max_length=5000)
    requires_approval: bool = True


class TaskResponse(BaseModel):
    task_id: str
    state: Literal["pending_approval", "accepted"]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskRequest) -> TaskResponse:
    """Create a local teaching task; replace in exercises, not in this scaffold."""
    task_id = str(uuid4())
    logger.info("task_created task_id=%s title_length=%s", task_id, len(payload.title))
    task_state: Literal["pending_approval", "accepted"] = (
        "pending_approval" if payload.requires_approval else "accepted"
    )
    return TaskResponse(task_id=task_id, state=task_state)


@app.post("/tasks/{task_id}/approve")
def approve_task(task_id: str) -> dict[str, str]:
    if not task_id.strip():
        raise HTTPException(status_code=400, detail="task_id must not be empty")
    # Independent task: persist status and add authorization before treating this as production code.
    return {"task_id": task_id, "state": "approved"}
