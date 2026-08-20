"""Chapter 12 teaching example: SQL 与 PostgreSQL."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LearningTask:
    title: str
    priority: int


def validate_task(title: str, priority: int) -> LearningTask:
    if not title.strip():
        raise ValueError("title must not be empty")
    if priority not in {1, 2, 3}:
        raise ValueError("priority must be 1, 2, or 3")
    return LearningTask(title=title.strip(), priority=priority)


if __name__ == "__main__":
    print(validate_task("SQL 与 PostgreSQL", 1))
