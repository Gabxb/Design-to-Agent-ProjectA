"""Pydantic models used at API, agent, tool, storage, and evaluation boundaries."""

from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class Role(str, Enum):
    STUDENT = "student"
    SUPPORT_AGENT = "support_agent"
    ADMIN = "admin"


class Principal(BaseModel):
    """Authenticated user identity. Never obtain this from model output."""

    model_config = ConfigDict(frozen=True)

    user_id: str = Field(min_length=3, max_length=64)
    tenant_id: str = Field(min_length=3, max_length=64)
    role: Role


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4_000)
    conversation_id: str = Field(default="demo", pattern=r"^[a-zA-Z0-9_-]{1,64}$")


class Citation(BaseModel):
    source_id: str
    title: str
    chunk_id: str
    score: float = Field(ge=0, le=1)


class ToolCall(BaseModel):
    call_id: str = Field(min_length=6, max_length=80)
    name: str = Field(min_length=3, max_length=64)
    arguments: dict[str, Any]


class ToolResult(BaseModel):
    call_id: str
    name: str
    ok: bool
    output: dict[str, Any]
    error_code: str | None = None


class PendingApproval(BaseModel):
    approval_id: str
    tool_call: ToolCall
    reason: str


class AgentReply(BaseModel):
    answer: str
    citations: list[Citation] = Field(default_factory=list)
    trace_id: str
    steps: int = Field(ge=0)
    pending_approval: PendingApproval | None = None


class AgentEventType(str, Enum):
    USER_MESSAGE = "user_message"
    MODEL_DECISION = "model_decision"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    FINAL = "final"
    APPROVAL_REQUIRED = "approval_required"


class AgentEvent(BaseModel):
    event_type: AgentEventType
    payload: dict[str, Any]


class AgentState(BaseModel):
    """Per-run, short-term state. Persist only redacted/necessary values in production."""

    conversation_id: str
    principal: Principal
    trace_id: str
    events: list[AgentEvent] = Field(default_factory=list)
    seen_fingerprints: set[str] = Field(default_factory=set)
    citations: list[Citation] = Field(default_factory=list)
    pending_approval: PendingApproval | None = None
    step: int = 0


class ModelDecision(BaseModel):
    """A constrained decision emitted by a model adapter or deterministic test double."""

    kind: Literal["final", "tool_call"]
    answer: str | None = Field(default=None, max_length=4_000)
    tool_call: ToolCall | None = None


class TicketDraft(BaseModel):
    title: str = Field(min_length=5, max_length=120)
    description: str = Field(min_length=10, max_length=2_000)
    priority: Literal["low", "normal", "high"] = "normal"


class EvaluationCase(BaseModel):
    case_id: str
    category: Literal[
        "task",
        "tool",
        "retrieval",
        "citation",
        "refusal",
        "permission",
        "prompt_injection",
    ]
    user_message: str
    principal: Principal
    expected: dict[str, Any]
