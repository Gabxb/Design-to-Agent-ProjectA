from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, TYPE_CHECKING
if TYPE_CHECKING:
    from app.agent.state import AgentState
    from app.agent.tools import ToolCall
@dataclass(frozen=True)
class ModelDecision:
    kind: str
    text: str | None = None
    tool_call: "ToolCall | None" = None
class ModelClient(Protocol):
    async def decide(self, *, state: "AgentState", tool_schemas: list[dict]) -> ModelDecision: ...
