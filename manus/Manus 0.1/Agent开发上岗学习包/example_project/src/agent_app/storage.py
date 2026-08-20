"""Small SQLite storage adapter for audit events and idempotency records.

For production, replace with SQLAlchemy/Alembic plus PostgreSQL and row-level policies.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class AuditStore:
    """Stores minimal audit metadata. Do not persist secrets or raw private context."""

    def __init__(self, database_url: str) -> None:
        if not database_url.startswith("sqlite:///"):
            raise ValueError("learning starter supports only sqlite:/// URLs")
        self._path = Path(database_url.removeprefix("sqlite:///"))

    def initialize(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS audit_events (
                    event_id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    trace_id TEXT NOT NULL,
                    tenant_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_audit_tenant_created
                ON audit_events(tenant_id, created_at DESC)
                """
            )

    def append_event(
        self,
        event_id: str,
        trace_id: str,
        tenant_id: str,
        user_id: str,
        event_type: str,
        payload: dict[str, Any],
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO audit_events(event_id, created_at, trace_id, tenant_id, user_id, event_type, payload_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event_id,
                    datetime.now(UTC).isoformat(),
                    trace_id,
                    tenant_id,
                    user_id,
                    event_type,
                    json.dumps(payload, ensure_ascii=False, sort_keys=True),
                ),
            )

    def list_for_tenant(self, tenant_id: str, limit: int = 100) -> list[dict[str, Any]]:
        """Tenant filter is mandatory; callers never get a cross-tenant list method."""

        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT event_id, created_at, trace_id, tenant_id, user_id, event_type, payload_json
                FROM audit_events WHERE tenant_id = ? ORDER BY created_at DESC LIMIT ?
                """,
                (tenant_id, limit),
            ).fetchall()
        return [
            {
                "event_id": row[0],
                "created_at": row[1],
                "trace_id": row[2],
                "tenant_id": row[3],
                "user_id": row[4],
                "event_type": row[5],
                "payload": json.loads(row[6]),
            }
            for row in rows
        ]

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._path)
