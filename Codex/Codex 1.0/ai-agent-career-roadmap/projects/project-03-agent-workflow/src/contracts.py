"""Initial API contracts; extend them as project requirements are implemented."""

from __future__ import annotations

from pydantic import BaseModel, Field


class TaskRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=20_000)


class TaskResponse(BaseModel):
    task_id: str
    project: str = "智能设计评审 Agent"
    status: str
