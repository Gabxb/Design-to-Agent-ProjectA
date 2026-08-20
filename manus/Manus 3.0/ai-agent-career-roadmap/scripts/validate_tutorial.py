#!/usr/bin/env python3
"""Validate book-first tutorial artifacts in addition to the base repository checks."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports/tutorial_validation_report.json"


def main() -> int:
    errors: list[str] = []
    base = subprocess.run([sys.executable, str(ROOT / "scripts/check_files.py"), "--require-pdfs"], cwd=ROOT, check=False)
    if base.returncode != 0:
        errors.append("base_repository_validation_failed")
    required = [
        "BOOK.md", "BOOK.html", "BOOK.pdf", "TABLE_OF_CONTENTS.md", "READING_GUIDE.md", "QUICK_REFERENCE.md",
        "generate_book.py", "update_book.py", "output/book/ai-agent-career-roadmap.md", "output/book/ai-agent-career-roadmap.html", "output/book/ai-agent-career-roadmap.pdf",
        "overview/OUTLINE.md", "overview/OUTLINE.pdf", "overview/ONE_PAGE_OVERVIEW.md", "overview/ONE_PAGE_OVERVIEW.pdf",
        "overview/LEARNING_MAP.mmd", "overview/LEARNING_MAP.svg", "overview/LEARNING_MAP.png", "overview/LEARNING_MAP.pdf",
        "overview/TECH_SKILL_MINDMAP.mmd", "overview/TECH_SKILL_MINDMAP.svg", "overview/TECH_SKILL_MINDMAP.png",
        "overview/ROADMAP_24_WEEKS.mmd", "overview/ROADMAP_24_WEEKS.svg", "overview/ROADMAP_24_WEEKS.png", "overview/ROADMAP_24_WEEKS.pdf",
        "overview/PROJECT_MAP.mmd", "overview/PROJECT_MAP.svg", "overview/PROJECT_MAP.png",
        "overview/JOB_SKILL_MATRIX.md", "overview/JOB_READY_PATH.md", "overview/JOB_READY_CHECKLIST.md",
        "output/GENERATION_REPORT.md", "output/VALIDATION_REPORT.md", "output/file-list.txt",
    ]
    for path in required:
        candidate = ROOT / path
        if not candidate.exists() or candidate.stat().st_size == 0:
            errors.append(f"missing_or_empty:{path}")
    chapters = list(ROOT.glob("book/part-*/chapter-*.md"))
    if len(chapters) != 70:
        errors.append(f"chapter_count:{len(chapters)}")
    for number in range(1, 7):
        for suffix in (".mmd", ".svg", ".png"):
            path = ROOT / f"overview/STAGE_{number:02d}_MAP{suffix}"
            if not path.exists() or path.stat().st_size == 0:
                errors.append(f"missing_stage_map:{path.relative_to(ROOT)}")
    for week in range(1, 25):
        for suffix in (".mmd", ".svg", ".png"):
            path = ROOT / f"weeks/week-{week:02d}/MINDMAP{suffix}"
            if not path.exists() or path.stat().st_size == 0:
                errors.append(f"missing_week_map:{path.relative_to(ROOT)}")
    for plan in ("plan-a-foundation", "plan-b-job-ready", "plan-c-designer-ai"):
        for filename in ("ROADMAP.md", "ROADMAP.pdf", "ROADMAP.mmd", "ROADMAP.svg", "WEEK_INDEX.md", "PROJECT_PATH.md", "RISKS.md"):
            path = ROOT / f"plans/{plan}/{filename}"
            if not path.exists() or path.stat().st_size == 0:
                errors.append(f"missing_plan_artifact:{path.relative_to(ROOT)}")
    for project in ("project-01-tool-calling", "project-02-rag-knowledge-base", "project-03-agent-workflow", "project-04-capstone"):
        for stem in ("ARCHITECTURE", "AGENT_WORKFLOW"):
            for suffix in (".md", ".mmd", ".svg", ".png"):
                path = ROOT / f"projects/{project}/{stem}{suffix}"
                if not path.exists() or path.stat().st_size == 0:
                    errors.append(f"missing_project_artifact:{path.relative_to(ROOT)}")
    if shutil.which("pdftotext"):
        result = subprocess.run(["pdftotext", str(ROOT / "BOOK.pdf"), "-"], text=True, capture_output=True, check=False)
        if result.returncode != 0 or "从设计师到 AI Agent" not in result.stdout:
            errors.append("book_pdf_text_or_cjk_validation_failed")
    compiled = subprocess.run([sys.executable, "-m", "compileall", "-q", "generate_book.py", "update_book.py", "scripts"], cwd=ROOT, check=False)
    if compiled.returncode != 0:
        errors.append("python_compile_failed")
    report = {"errors": errors, "chapter_count": len(chapters), "book_pdf_bytes": (ROOT / "BOOK.pdf").stat().st_size if (ROOT / "BOOK.pdf").exists() else 0}
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Tutorial validation: {len(errors)} error(s); 70-chapter target found {len(chapters)} files.")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
