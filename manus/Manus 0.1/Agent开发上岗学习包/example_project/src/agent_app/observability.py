"""Minimal structured logging and trace helpers.

Use OpenTelemetry or a managed tracing backend in production; this module keeps the
learning project observable without coupling tests to external infrastructure.
"""

from __future__ import annotations

import logging
import sys
from contextvars import ContextVar
from typing import cast
from uuid import uuid4

import structlog

_trace_id: ContextVar[str | None] = ContextVar("trace_id", default=None)


def configure_logging(level: str) -> None:
    """Configure JSON structured logs once during application startup."""

    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=level.upper())
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def new_trace_id() -> str:
    """Create and bind a request trace identifier."""

    trace_id = uuid4().hex
    _trace_id.set(trace_id)
    structlog.contextvars.bind_contextvars(trace_id=trace_id)
    return trace_id


def get_logger(component: str) -> structlog.stdlib.BoundLogger:
    """Return a component-bound logger. Callers must avoid PII and secrets."""

    return cast(structlog.stdlib.BoundLogger, structlog.get_logger().bind(component=component))
