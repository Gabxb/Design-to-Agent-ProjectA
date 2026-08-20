from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Protocol

from pydantic import BaseModel, Field, ValidationError

from app.core.errors import PermissionDenied, ToolExecutionError
from app.schemas import PermissionContext


class TicketLookupArgs(BaseModel):
    ticket_id: str = Field(min_length=3, max_length=64)


class CreateTicketArgs(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    body: str = Field(min_length=1, max_length=4000)
    idempotency_key: str = Field(min_length=8, max_length=128)
    approval_id: str = Field(min_length=8, max_length=128)


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, Any]


@dataclass
class ToolDef:
    name: str
    description: str
    input_model: type[BaseModel]
    handler: Callable[[BaseModel, PermissionContext], Awaitable[dict[str, Any]]]
    risk: str = "read"


class ApprovalChecker(Protocol):
    async def __call__(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        ctx: PermissionContext,
    ) -> bool: ...


class ToolRegistry:
    """Server-side tool registry.

    Validation and permission checks happen here rather than trusting model output.
    High-risk write tools fail closed unless a server-side approval checker confirms
    that the supplied approval_id is valid for the current user/tenant/tool/payload.
    """

    def __init__(self, approval_checker: ApprovalChecker | None = None) -> None:
        self._tools: dict[str, ToolDef] = {}
        self._approval_checker = approval_checker

    def register(self, tool: ToolDef) -> None:
        if tool.name in self._tools:
            raise ValueError(f"duplicate tool: {tool.name}")
        self._tools[tool.name] = tool

    def schemas(self) -> list[dict[str, Any]]:
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.input_model.model_json_schema(),
            }
            for tool in self._tools.values()
        ]

    async def execute(self, call: ToolCall, ctx: PermissionContext) -> dict[str, Any]:
        tool = self._tools.get(call.name)
        if tool is None:
            raise ToolExecutionError("unknown_tool", retryable=False)

        try:
            args = tool.input_model.model_validate(call.arguments)
        except ValidationError as exc:
            raise ToolExecutionError("invalid_tool_arguments", retryable=False) from exc

        if tool.risk == "write":
            if "ticket:write" not in ctx.permissions:
                raise PermissionDenied("ticket:write required")
            approval_id = getattr(args, "approval_id", None)
            if not approval_id or self._approval_checker is None:
                raise PermissionDenied("valid human approval required")
            approved = await self._approval_checker(call.name, args.model_dump(), ctx)
            if not approved:
                raise PermissionDenied("approval rejected or expired")

        return await tool.handler(args, ctx)
