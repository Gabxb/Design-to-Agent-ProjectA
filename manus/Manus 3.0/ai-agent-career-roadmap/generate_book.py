#!/usr/bin/env python3
"""One-command generator for the local 24-week AI Agent tutorial book."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(script: str) -> None:
    result = subprocess.run([sys.executable, str(ROOT / script)], cwd=ROOT, check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main() -> int:
    run("scripts/upgrade_tutorial.py")
    run("scripts/generate_plan_artifacts.py")
    run("scripts/generate_stage_maps.py")
    run("scripts/generate_mindmaps.py")
    run("scripts/build_book.py")
    run("scripts/build_book_pdf.py")
    run("scripts/build_auxiliary_pdfs.py")
    run("scripts/refresh_manifest.py")
    run("scripts/validate_tutorial.py")
    run("scripts/create_output_reports.py")
    print("Complete tutorial book build finished. Start with BOOK.md or output/book/ai-agent-career-roadmap.html.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
