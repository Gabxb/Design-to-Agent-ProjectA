from __future__ import annotations

from agent_app.agent_loop import AgentRunner
from agent_app.config import Settings
from agent_app.model_client import ScriptedModelClient
from agent_app.schemas import ModelDecision, Principal, Role, ToolCall
from agent_app.tools import ToolRegistry


def make_settings(**overrides: object) -> Settings:
    return Settings(model_api_key="test-key", **overrides)


def make_principal(role: Role = Role.SUPPORT_AGENT) -> Principal:
    return Principal(user_id="user-001", tenant_id="tenant-a", role=role)


async def no_sleep(_: float) -> None:
    return None


async def test_search_tool_yields_citations() -> None:
    model = ScriptedModelClient(
        [
            ModelDecision(
                kind="tool_call",
                tool_call=ToolCall(
                    call_id="call-001",
                    name="search_knowledge",
                    arguments={"query": "如何创建工单", "top_k": 2},
                ),
            ),
            ModelDecision(kind="final", answer="请先展示工单草稿并取得人工确认。"),
        ]
    )
    runner = AgentRunner(make_settings(), model, ToolRegistry(make_settings()), sleep=no_sleep)

    reply = await runner.run("如何创建工单？", "conversation-1", make_principal(), "trace-1")

    assert reply.answer.startswith("请先展示")
    assert len(reply.citations) == 2
    assert reply.steps == 2


async def test_student_cannot_read_ticket() -> None:
    model = ScriptedModelClient(
        [
            ModelDecision(
                kind="tool_call",
                tool_call=ToolCall(call_id="call-002", name="get_ticket", arguments={"ticket_id": "TCK-0001"}),
            ),
            ModelDecision(kind="final", answer="无权读取该工单，建议联系支持人员。"),
        ]
    )
    runner = AgentRunner(make_settings(), model, ToolRegistry(make_settings()), sleep=no_sleep)

    reply = await runner.run("查询 TCK-0001", "conversation-2", make_principal(Role.STUDENT), "trace-2")

    assert "无权" in reply.answer
    assert reply.pending_approval is None


async def test_write_tool_requires_human_approval() -> None:
    model = ScriptedModelClient(
        [
            ModelDecision(
                kind="tool_call",
                tool_call=ToolCall(
                    call_id="call-003",
                    name="draft_ticket",
                    arguments={
                        "title": "无法登录企业系统",
                        "description": "用户在单点登录后持续收到权限错误，需要支持团队调查。",
                        "priority": "normal",
                        "idempotency_key": "request-0003",
                    },
                ),
            )
        ]
    )
    runner = AgentRunner(make_settings(enable_write_tools=True), model, ToolRegistry(make_settings(enable_write_tools=True)), sleep=no_sleep)

    reply = await runner.run("帮我创建工单", "conversation-3", make_principal(), "trace-3")

    assert reply.pending_approval is not None
    assert reply.pending_approval.tool_call.name == "draft_ticket"


async def test_duplicate_call_is_rejected() -> None:
    model = ScriptedModelClient(
        [
            ModelDecision(
                kind="tool_call",
                tool_call=ToolCall(call_id="call-004a", name="search_knowledge", arguments={"query": "工单", "top_k": 1}),
            ),
            ModelDecision(
                kind="tool_call",
                tool_call=ToolCall(call_id="call-004b", name="search_knowledge", arguments={"query": "工单", "top_k": 1}),
            ),
            ModelDecision(kind="final", answer="已完成检索。"),
        ]
    )
    runner = AgentRunner(make_settings(), model, ToolRegistry(make_settings()), sleep=no_sleep)

    reply = await runner.run("检索工单", "conversation-4", make_principal(), "trace-4")

    assert reply.answer == "已完成检索。"
    assert reply.steps == 3
