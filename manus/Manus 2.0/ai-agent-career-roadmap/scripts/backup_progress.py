#!/usr/bin/env python3
"""Create a timestamped backup of mutable learning records."""
from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / ".backups" / f"manual-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
FILES = [
    "progress/progress.json",
    "progress/DAILY_LOG.md",
    "progress/WEEKLY_STATUS.md",
    "progress/SKILL_PROGRESS.md",
    "progress/PROBLEMS.md",
    "progress/COMPLETED_TASKS.md",
    "config/current_plan.yaml",
]


def main() -> int:
    for relative in FILES:
        source = ROOT / relative
        if source.exists():
            destination = TARGET / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
    print(f"Backup created: {TARGET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
