"""FastAPI entry point for the secure agent learning starter."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, status

from agent_app.agent_loop import AgentRunner
from agent_app.config import Settings, get_settings
from agent_app.model_client import OpenAIResponsesClient
from agent_app.observability import configure_logging, new_trace_id
from agent_app.schemas import AgentReply, ChatRequest, Principal, Role
from agent_app.tools import ToolRegistry


def get_principal(
    x_user_id: Annotated[str | None, Header()] = None,
    x_tenant_id: Annotated[str | None, Header()] = None,
    x_role: Annotated[Role | None, Header()] = None,
) -> Principal:
    """Teaching-only identity adapter. Replace with verified JWT/session middleware.

    Header values are accepted solely to make local testing easy. Production must derive
    user, tenant, and role from a signature-verified credential, never model output.
    """

    if not x_user_id or not x_tenant_id or x_role is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing authenticated principal")
    return Principal(user_id=x_user_id, tenant_id=x_tenant_id, role=x_role)


def build_runner(settings: Settings) -> AgentRunner:
    return AgentRunner(
        settings=settings,
        model_client=OpenAIResponsesClient(settings),
        tools=ToolRegistry(settings),
    )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    settings = get_settings()
    configure_logging(settings.log_level)
    app.state.runner = build_runner(settings)
    yield


app = FastAPI(title="Secure Agent Starter", version="0.1.0", lifespan=lifespan)


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/chat", response_model=AgentReply)
async def chat(
    request: ChatRequest,
    principal: Annotated[Principal, Depends(get_principal)],
) -> AgentReply:
    trace_id = new_trace_id()
    runner: AgentRunner = app.state.runner
    return await runner.run(
        message=request.message,
        conversation_id=request.conversation_id,
        principal=principal,
        trace_id=trace_id,
    )
