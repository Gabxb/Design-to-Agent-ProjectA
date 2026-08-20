#!/usr/bin/env python3
"""Render overview and plan Markdown sources to local CJK PDFs."""
from __future__ import annotations

from pathlib import Path

import markdown
from weasyprint import HTML

ROOT = Path(__file__).resolve().parents[1]

SOURCES = [
    "overview/OUTLINE.md",
    "overview/ONE_PAGE_OVERVIEW.md",
    "overview/LEARNING_MAP.md",
    "overview/ROADMAP_24_WEEKS.md",
    "overview/TECH_SKILL_MINDMAP.md",
    "overview/PROJECT_MAP.md",
    "plans/plan-a-foundation/ROADMAP.md",
    "plans/plan-b-job-ready/ROADMAP.md",
    "plans/plan-c-designer-ai/ROADMAP.md",
]

CSS = """
@page { size: A4; margin: 18mm 16mm 18mm; @bottom-center { content: counter(page); color: #587080; font-size: 9pt; } }
body { font-family: 'Noto Sans CJK SC', 'Microsoft YaHei', sans-serif; color: #16202A; line-height: 1.65; font-size: 10pt; }
h1 { color: #102A43; border-bottom: 2px solid #2F80ED; padding-bottom: 5pt; }
h2 { color: #1F4E79; margin-top: 18pt; }
table { border-collapse: collapse; width: 100%; font-size: 8.6pt; } th, td { border: 1px solid #D7E2E8; padding: 5pt; vertical-align: top; } th { background: #EEF5FB; }
pre { white-space: pre-wrap; overflow-wrap: anywhere; background: #102A43; color: #E9F4FF; padding: 8pt; }
img { max-width: 100%; max-height: 210mm; object-fit: contain; }
a { color: #1769AA; }
"""


def render(source: Path) -> None:
    body = markdown.markdown(source.read_text(encoding="utf-8"), extensions=["extra", "tables", "fenced_code", "toc"])
    html = f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"
    HTML(string=html, base_url=str(ROOT)).write_pdf(str(source.with_suffix(".pdf")))


def main() -> int:
    count = 0
    for relative in SOURCES:
        source = ROOT / relative
        if source.exists():
            render(source)
            count += 1
            print(f"OK {source.with_suffix('.pdf').relative_to(ROOT)}")
    print(f"Built {count} auxiliary PDFs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
