"""A deliberately small, inspectable Agent Loop for learning and tests."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable

from agent_app.config import Settings
from agent_app.model_client import ModelClient, NonRetryableModelError, RetryableModelError
from agent_app.observability import get_logger
from agent_app.schemas import (
    AgentEvent,
    AgentEventType,
    AgentReply,
    AgentState,
    ModelDecision,
    Principal,
    ToolCall,
    ToolResult,
)
from agent_app.tools import ToolRegistry

logger = get_logger("agent_loop")

Sleep = Callable[[float], Awaitable[None]]


class AgentRunner:
    """Runs one bounded agent interaction. It never delegates authorization to the model."""

    def __init__(
        self,
        settings: Settings,
        model_client: ModelClient,
        tools: ToolRegistry,
        sleep: Sleep = asyncio.sleep,
    ) -> None:
        self._settings = settings
        self._model_client = model_client
        self._tools = tools
        self._sleep = sleep

    async def run(self, message: str, conversation_id: str, principal: Principal, trace_id: str) -> AgentReply:
        state = AgentState(conversation_id=conversation_id, principal=principal, trace_id=trace_id)
        state.events.append(AgentEvent(event_type=AgentEventType.USER_MESSAGE, payload={"message": message}))

        for step in range(1, self._settings.max_agent_steps + 1):
            state.step = step
            decision = await self._get_decision_with_bounded_retry(state)
            if decision.kind == "final":
                answer = decision.answer or "模型未返回可用答案。"
                state.events.append(AgentEvent(event_type=AgentEventType.FINAL, payload={"answer": answer}))
                return AgentReply(
                    answer=answer,
                    citations=state.citations,
                    trace_id=trace_id,
                    steps=step,
                    pending_approval=state.pending_approval,
                )

            assert decision.tool_call is not None
            result = await self._execute_tool(decision.tool_call, state)
            if result.error_code == "approval_required":
                state.events.append(
                    AgentEvent(
                        event_type=AgentEventType.APPROVAL_REQUIRED,
                        payload={"tool": decision.tool_call.name, "approval_id": state.pending_approval.approval_id if state.pending_approval else None},
                    )
                )
                return AgentReply(
                    answer="已生成待确认的高风险操作草稿；请由有权限的用户审核并确认。",
                    citations=state.citations,
                    trace_id=trace_id,
                    steps=step,
                    pending_approval=state.pending_approval,
                )
            state.events.append(
                AgentEvent(
                    event_type=AgentEventType.TOOL_RESULT,
                    payload={"tool": result.name, "ok": result.ok, "output": result.output, "error_code": result.error_code},
                )
            )

        return AgentReply(
            answer="为避免无限循环，系统已达到最大执行步数。请缩小问题范围或交由人工处理。",
            citations=state.citations,
            trace_id=trace_id,
            steps=self._settings.max_agent_steps,
            pending_approval=state.pending_approval,
        )

    async def _get_decision_with_bounded_retry(self, state: AgentState) -> ModelDecision:
        tools = self._tools.schemas_for(state)
        for attempt in range(self._settings.max_tool_retries + 1):
            try:
                decision = await self._model_client.decide(state, tools)
                state.events.append(
                    AgentEvent(
                        event_type=AgentEventType.MODEL_DECISION,
                        payload={"kind": decision.kind, "tool": decision.tool_call.name if decision.tool_call else None},
                    )
                )
                return decision
            except RetryableModelError as exc:
                if attempt >= self._settings.max_tool_retries:
                    logger.warning("model_retry_exhausted", attempt=attempt, error=str(exc))
                    return _fallback_decision()
                await self._sleep(0.25 * (2**attempt))
            except NonRetryableModelError as exc:
                logger.warning("model_non_retryable_error", error=str(exc))
                return _fallback_decision()
        return _fallback_decision()

    async def _execute_tool(self, call: ToolCall, state: AgentState) -> ToolResult:
        state.events.append(AgentEvent(event_type=AgentEventType.TOOL_CALL, payload={"tool": call.name}))
        try:
            return await asyncio.wait_for(
                self._tools.execute(call, state), timeout=self._settings.request_timeout_seconds
            )
        except TimeoutError:
            logger.warning("tool_timeout", tool=call.name)
            return ToolResult(call_id=call.call_id, name=call.name, ok=False, output={}, error_code="tool_timeout")


def _fallback_decision() -> ModelDecision:
    return ModelDecision(kind="final", answer="当前模型服务不可用，未执行任何写操作。请稍后重试或交由人工处理。")
