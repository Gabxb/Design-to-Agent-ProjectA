#!/usr/bin/env python3
"""Check all local Markdown links by delegating to the repository validator."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    result = subprocess.run([sys.executable, str(ROOT / "scripts/check_files.py"), "--require-pdfs"], cwd=ROOT, check=False)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
