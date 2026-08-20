"""Permission-aware tool registry. The model proposes calls; the server authorizes execution."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, ValidationError

from agent_app.config import Settings
from agent_app.observability import get_logger
from agent_app.schemas import AgentState, Citation, PendingApproval, Role, TicketDraft, ToolCall, ToolResult

logger = get_logger("tools")


class ToolError(RuntimeError):
    """A safe tool failure that may be returned to the model without infrastructure detail."""


class AuthorizationError(ToolError):
    """Raised when the authenticated principal cannot invoke a tool."""


class DuplicateToolCallError(ToolError):
    """Raised when an identical operation occurs in the same agent run."""


class SearchKnowledgeInput(BaseModel):
    query: str = Field(min_length=2, max_length=300)
    top_k: int = Field(default=3, ge=1, le=5)


class GetTicketInput(BaseModel):
    ticket_id: str = Field(pattern=r"^TCK-[0-9]{4}$")


class DraftTicketInput(TicketDraft):
    idempotency_key: str = Field(min_length=8, max_length=128)


ToolHandler = Callable[[BaseModel, AgentState], Awaitable[dict[str, Any]]]


@dataclass(frozen=True)
class RegisteredTool:
    name: str
    description: str
    input_model: type[BaseModel]
    handler: ToolHandler
    allowed_roles: frozenset[Role]
    requires_approval: bool = False

    def schema(self) -> dict[str, object]:
        return {
            "type": "function",
            "name": self.name,
            "description": self.description,
            "parameters": self.input_model.model_json_schema(),
            "strict": True,
        }


class ToolRegistry:
    """Registry that validates, authorizes, de-duplicates, and executes tools."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._tools: dict[str, RegisteredTool] = {}
        self._ticket_drafts_by_idempotency_key: dict[str, dict[str, Any]] = {}
        self.register(
            RegisteredTool(
                name="search_knowledge",
                description="Search only documents visible to the authenticated user. Use for policy or product facts.",
                input_model=SearchKnowledgeInput,
                handler=self._search_knowledge,
                allowed_roles=frozenset({Role.STUDENT, Role.SUPPORT_AGENT, Role.ADMIN}),
            )
        )
        self.register(
            RegisteredTool(
                name="get_ticket",
                description="Read one support ticket in the caller's tenant. Never use for another tenant.",
                input_model=GetTicketInput,
                handler=self._get_ticket,
                allowed_roles=frozenset({Role.SUPPORT_AGENT, Role.ADMIN}),
            )
        )
        self.register(
            RegisteredTool(
                name="draft_ticket",
                description="Create a reversible ticket draft only. Requires explicit human approval before execution.",
                input_model=DraftTicketInput,
                handler=self._draft_ticket,
                allowed_roles=frozenset({Role.SUPPORT_AGENT, Role.ADMIN}),
                requires_approval=True,
            )
        )

    def register(self, tool: RegisteredTool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"duplicate tool registration: {tool.name}")
        self._tools[tool.name] = tool

    def schemas_for(self, state: AgentState) -> list[dict[str, object]]:
        """Expose only tools this principal can potentially use; do not leak admin tools."""

        return [tool.schema() for tool in self._tools.values() if state.principal.role in tool.allowed_roles]

    async def execute(self, call: ToolCall, state: AgentState, approved: bool = False) -> ToolResult:
        tool = self._tools.get(call.name)
        if tool is None:
            return ToolResult(call_id=call.call_id, name=call.name, ok=False, output={}, error_code="unknown_tool")
        if state.principal.role not in tool.allowed_roles:
            return ToolResult(call_id=call.call_id, name=call.name, ok=False, output={}, error_code="forbidden")

        fingerprint = self._fingerprint(call, state)
        if fingerprint in state.seen_fingerprints:
            return ToolResult(call_id=call.call_id, name=call.name, ok=False, output={}, error_code="duplicate_call")

        try:
            validated = tool.input_model.model_validate(call.arguments)
        except ValidationError:
            return ToolResult(call_id=call.call_id, name=call.name, ok=False, output={}, error_code="invalid_arguments")

        if tool.requires_approval and not approved:
            state.pending_approval = PendingApproval(
                approval_id=uuid4().hex,
                tool_call=call,
                reason="该操作会创建工单草稿，必须先由已登录用户确认。",
            )
            return ToolResult(call_id=call.call_id, name=call.name, ok=False, output={}, error_code="approval_required")
        if tool.requires_approval and not self._settings.enable_write_tools:
            return ToolResult(call_id=call.call_id, name=call.name, ok=False, output={}, error_code="write_tools_disabled")

        state.seen_fingerprints.add(fingerprint)
        try:
            output = await tool.handler(validated, state)
        except AuthorizationError:
            return ToolResult(call_id=call.call_id, name=call.name, ok=False, output={}, error_code="forbidden")
        except ToolError as exc:
            logger.warning("tool_failed", tool=call.name, error_code=str(exc))
            return ToolResult(call_id=call.call_id, name=call.name, ok=False, output={}, error_code=str(exc))
        return ToolResult(call_id=call.call_id, name=call.name, ok=True, output=output)

    @staticmethod
    def _fingerprint(call: ToolCall, state: AgentState) -> str:
        raw = json.dumps(
            {"tenant": state.principal.tenant_id, "name": call.name, "arguments": call.arguments},
            sort_keys=True,
            ensure_ascii=False,
        )
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    async def _search_knowledge(self, payload: BaseModel, state: AgentState) -> dict[str, Any]:
        args = SearchKnowledgeInput.model_validate(payload)
        # A teaching stub: retrieve only records carrying the caller's tenant ACL.
        corpus = [
            {
                "tenant_id": state.principal.tenant_id,
                "source_id": "policy-001",
                "title": "企业服务工单规范",
                "chunk_id": "policy-001#refund",
                "text": "退款类请求需先核验订单状态；创建工单前必须展示草稿并取得人工确认。",
                "score": 0.91,
            },
            {
                "tenant_id": state.principal.tenant_id,
                "source_id": "runbook-002",
                "title": "值班升级手册",
                "chunk_id": "runbook-002#severity",
                "text": "高优先级事故应收集影响范围、时间窗口和已完成的缓解措施。",
                "score": 0.79,
            },
        ]
        visible = [item for item in corpus if item["tenant_id"] == state.principal.tenant_id]
        matches = visible[: args.top_k]
        citations = [
            Citation(
                source_id=str(item["source_id"]),
                title=str(item["title"]),
                chunk_id=str(item["chunk_id"]),
                score=float(str(item["score"])),
            )
            for item in matches
        ]
        state.citations = citations
        return {"query": args.query, "matches": matches, "citations": [c.model_dump() for c in citations]}

    async def _get_ticket(self, payload: BaseModel, state: AgentState) -> dict[str, Any]:
        args = GetTicketInput.model_validate(payload)
        # Tenant is derived from `state.principal`, never from tool arguments.
        return {
            "ticket_id": args.ticket_id,
            "tenant_id": state.principal.tenant_id,
            "status": "open",
            "summary": "演示工单：等待进一步信息。",
        }

    async def _draft_ticket(self, payload: BaseModel, state: AgentState) -> dict[str, Any]:
        args = DraftTicketInput.model_validate(payload)
        existing = self._ticket_drafts_by_idempotency_key.get(args.idempotency_key)
        if existing is not None:
            return existing
        draft = {
            "draft_id": f"DRF-{uuid4().hex[:8]}",
            "tenant_id": state.principal.tenant_id,
            "title": args.title,
            "description": args.description,
            "priority": args.priority,
            "status": "draft",
        }
        self._ticket_drafts_by_idempotency_key[args.idempotency_key] = draft
        return draft
