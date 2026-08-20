#!/usr/bin/env python3
"""Create the book PDF from BOOK.md via the generated offline HTML reading edition.

Markdown remains the single source: build_book.py creates BOOK.html from BOOK.md,
and this script renders that local HTML with embedded maps into a paginated CJK PDF.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from weasyprint import HTML

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output/book"
SKILL = Path("/home/ubuntu/skills/typst-pdf-maker/scripts")


def main() -> int:
    source = ROOT / "BOOK.html"
    if not source.exists():
        print("BOOK.html is missing. Run python scripts/build_book.py first.", file=sys.stderr)
        return 2
    OUTPUT.mkdir(parents=True, exist_ok=True)
    target = ROOT / "BOOK.pdf"
    try:
        HTML(filename=str(source), base_url=str(ROOT)).write_pdf(str(target))
    except Exception as error:  # noqa: BLE001
        print(f"HTML to PDF conversion failed: {error}", file=sys.stderr)
        return 1
    if not target.exists() or target.stat().st_size < 5000:
        print("Generated PDF is missing or too small.", file=sys.stderr)
        return 1
    output_pdf = OUTPUT / "ai-agent-career-roadmap.pdf"
    shutil.copy2(target, output_pdf)
    if (SKILL / "verify_pdf.py").exists():
        verified = subprocess.run([sys.executable, str(SKILL / "verify_pdf.py"), str(target), "--profile", "text-document"], cwd=ROOT, check=False)
        if verified.returncode != 0:
            return verified.returncode
    print("Built and verified BOOK.pdf from the offline HTML edition.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
