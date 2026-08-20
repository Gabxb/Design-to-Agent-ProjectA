from __future__ import annotations
from dataclasses import dataclass, field
from uuid import uuid4
from app.schemas import PermissionContext
@dataclass
class AgentState:
    run_id: str
    user_message: str
    permission_context: PermissionContext
    step: int = 0
    observations: list[dict] = field(default_factory=list)
    final_answer: str | None = None
    status: str = "running"
    error: str | None = None
    @classmethod
    def new(cls, message: str, ctx: PermissionContext) -> "AgentState": return cls(str(uuid4()), message, ctx)
    def as_model_input(self):
        return [{"role":"system","content":"Use tools only when needed. Never infer permissions."},
                {"role":"user","content":self.user_message},
                {"role":"user","content":f"Observations: {self.observations}"}]
