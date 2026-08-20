#!/usr/bin/env python3
"""Generate requested CJK PDFs from Markdown source files using Typst.

The Markdown files remain the source of truth. The script creates temporary Typst
build folders under `.pdf-build/` and copies the final PDF beside each Markdown
file with the same base name.

Usage:
    python scripts/pdf_from_markdown.py --all
    python scripts/pdf_from_markdown.py --file roadmap/24_WEEK_ROADMAP.md
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = Path("/home/ubuntu/skills/typst-pdf-maker/scripts")
BUILD_ROOT = ROOT / ".pdf-build"


def requested_sources() -> list[Path]:
    sources = [
        ROOT / "plans/PLAN_COMPARISON.md",
        ROOT / "roadmap/24_WEEK_ROADMAP.md",
        ROOT / "roadmap/JOB_READY_CHECKLIST.md",
    ]
    sources.extend(ROOT / f"weeks/week-{week:02d}/WEEK_PLAN.md" for week in range(1, 25))
    for directory in ("project-01-tool-calling", "project-02-rag-knowledge-base", "project-03-agent-workflow", "project-04-capstone"):
        sources.append(ROOT / f"projects/{directory}/REQUIREMENTS.md")
        sources.append(ROOT / f"projects/{directory}/ARCHITECTURE.md")
    return sources


def require_tools() -> None:
    if shutil.which("typst") is None:
        raise RuntimeError("Typst is not installed. Install Typst or use a system with Typst available.")
    for filename in ("prepare_document.py", "generate_pdf.py", "verify_pdf.py"):
        if not (SKILL / filename).exists():
            raise RuntimeError(f"Required PDF helper is unavailable: {SKILL / filename}")


def build(source: Path) -> bool:
    if not source.exists():
        print(f"SKIP missing source: {source.relative_to(ROOT)}")
        return False
    safe_name = source.relative_to(ROOT).as_posix().replace("/", "__").replace(".md", "")
    workdir = BUILD_ROOT / safe_name
    if workdir.exists():
        shutil.rmtree(workdir)
    workdir.parent.mkdir(parents=True, exist_ok=True)
    prepare = [sys.executable, str(SKILL / "prepare_document.py"), "markdown", str(source), str(workdir)]
    prepared = subprocess.run(prepare, cwd=ROOT, text=True, capture_output=True, check=False)
    if prepared.returncode != 0:
        print(f"FAIL prepare {source.relative_to(ROOT)}\n{prepared.stderr[-1200:]}")
        return False
    compile_command = [sys.executable, str(SKILL / "generate_pdf.py"), str(workdir / "main.typ"), "--strict"]
    compiled = subprocess.run(compile_command, cwd=ROOT, text=True, capture_output=True, check=False)
    if compiled.returncode != 0:
        print(f"FAIL compile {source.relative_to(ROOT)}\n{compiled.stderr[-1200:]}\n{compiled.stdout[-1200:]}")
        return False
    built_pdf = workdir / "main.pdf"
    target_pdf = source.with_suffix(".pdf")
    if not built_pdf.exists() or built_pdf.stat().st_size < 500:
        print(f"FAIL empty PDF for {source.relative_to(ROOT)}")
        return False
    shutil.copy2(built_pdf, target_pdf)
    verifier = [sys.executable, str(SKILL / "verify_pdf.py"), str(target_pdf), "--profile", "text-document"]
    verified = subprocess.run(verifier, cwd=ROOT, text=True, capture_output=True, check=False)
    if verified.returncode != 0:
        print(f"FAIL verify {source.relative_to(ROOT)}\n{verified.stderr[-800:]}\n{verified.stdout[-800:]}")
        return False
    print(f"OK {target_pdf.relative_to(ROOT)}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Create CJK PDFs from Markdown source files.")
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--all", action="store_true", help="Generate every required PDF.")
    selection.add_argument("--file", help="Generate one PDF from a path relative to repository root.")
    args = parser.parse_args()
    try:
        require_tools()
    except RuntimeError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    sources = requested_sources() if args.all else [ROOT / args.file]
    results = [build(source) for source in sources]
    failed = len(results) - sum(results)
    print(f"PDF generation complete: {sum(results)} succeeded, {failed} failed.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
