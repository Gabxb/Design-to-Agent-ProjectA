import pytest

from app.agent.tools import CreateTicketArgs, ToolCall, ToolDef, ToolRegistry
from app.core.errors import PermissionDenied
from app.schemas import PermissionContext
from app.storage.db import IdempotencyStore, init_db, make_engine


@pytest.mark.asyncio
async def test_write_tool_fails_closed_without_approval_checker() -> None:
    async def create_ticket(args, ctx):
        return {"created": True}

    tools = ToolRegistry()
    tools.register(
        ToolDef(
            "create_ticket",
            "create ticket",
            CreateTicketArgs,
            create_ticket,
            risk="write",
        )
    )
    ctx = PermissionContext(
        user_id="u1",
        tenant_id="acme",
        permissions={"ticket:write"},
    )
    with pytest.raises(PermissionDenied):
        await tools.execute(
            ToolCall(
                "create_ticket",
                {
                    "title": "Example",
                    "body": "Body",
                    "idempotency_key": "idem-12345678",
                    "approval_id": "approval-12345678",
                },
            ),
            ctx,
        )


def test_idempotency_store_returns_original_result() -> None:
    engine = make_engine("sqlite+pysqlite:///:memory:")
    init_db(engine)
    store = IdempotencyStore(engine)
    assert store.put_once("acme", "key-12345678", {"ticket_id": "T-1"}) is True
    assert store.put_once("acme", "key-12345678", {"ticket_id": "T-2"}) is False
    assert store.get("acme", "key-12345678") == {"ticket_id": "T-1"}
