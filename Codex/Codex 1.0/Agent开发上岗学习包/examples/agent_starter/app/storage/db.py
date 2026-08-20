from __future__ import annotations

import json
from typing import Any

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


def make_engine(url: str) -> Engine:
    return create_engine(url, pool_pre_ping=True)


def init_db(engine: Engine) -> None:
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS idempotency (
                    tenant_id TEXT NOT NULL,
                    key TEXT NOT NULL,
                    result TEXT NOT NULL,
                    PRIMARY KEY (tenant_id, key)
                )
                """
            )
        )


class IdempotencyStore:
    """Small SQL-backed idempotency store for high-risk write tools."""

    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def get(self, tenant_id: str, key: str) -> dict[str, Any] | None:
        with self._engine.begin() as conn:
            row = conn.execute(
                text(
                    "SELECT result FROM idempotency "
                    "WHERE tenant_id = :tenant_id AND key = :key"
                ),
                {"tenant_id": tenant_id, "key": key},
            ).scalar_one_or_none()
        return None if row is None else json.loads(row)

    def put_once(self, tenant_id: str, key: str, result: dict[str, Any]) -> bool:
        payload = json.dumps(result, ensure_ascii=False, separators=(",", ":"))
        with self._engine.begin() as conn:
            existing = conn.execute(
                text(
                    "SELECT 1 FROM idempotency "
                    "WHERE tenant_id = :tenant_id AND key = :key"
                ),
                {"tenant_id": tenant_id, "key": key},
            ).scalar_one_or_none()
            if existing is not None:
                return False
            conn.execute(
                text(
                    "INSERT INTO idempotency (tenant_id, key, result) "
                    "VALUES (:tenant_id, :key, :result)"
                ),
                {"tenant_id": tenant_id, "key": key, "result": payload},
            )
        return True
