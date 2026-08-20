from __future__ import annotations

from agent_app.storage import AuditStore


def test_audit_store_is_tenant_scoped(tmp_path) -> None:
    store = AuditStore(f"sqlite:///{tmp_path / 'audit.db'}")
    store.initialize()
    store.append_event("evt-1", "trace-1", "tenant-a", "u-a", "tool_call", {"tool": "search"})
    store.append_event("evt-2", "trace-2", "tenant-b", "u-b", "tool_call", {"tool": "ticket"})

    rows = store.list_for_tenant("tenant-a")

    assert len(rows) == 1
    assert rows[0]["tenant_id"] == "tenant-a"
    assert rows[0]["payload"]["tool"] == "search"
