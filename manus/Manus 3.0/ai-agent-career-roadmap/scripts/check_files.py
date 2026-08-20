#!/usr/bin/env python3
"""Validate the local AI Agent learning system without modifying user notes."""
from __future__ import annotations

import argparse
import ast
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports/validation_report.json"

REQUIRED_ROOT = [
    "README.md", "START_HERE.md", "CHANGELOG.md", "LICENSE", "requirements.txt", ".gitignore", ".env.example", "generate_files.py", "update_plan.py",
    "config/learner_profile.yaml", "config/current_plan.yaml", "config/learning_settings.yaml", "config/file_manifest.json",
    "plans/PLAN_COMPARISON.md", "roadmap/24_WEEK_ROADMAP.md", "roadmap/SKILL_MATRIX.md", "roadmap/JOB_READY_CHECKLIST.md",
    "progress/progress.json", "progress/DAILY_LOG.md", "progress/WEEKLY_STATUS.md", "progress/SKILL_PROGRESS.md", "progress/PROBLEMS.md", "progress/COMPLETED_TASKS.md",
]
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)(api[_-]?key|secret|token)\s*=\s*['\"][^'\"]{12,}['\"]"),
]


def required_pdfs() -> list[Path]:
    paths = [
        ROOT / "plans/PLAN_COMPARISON.pdf",
        ROOT / "roadmap/24_WEEK_ROADMAP.pdf",
        ROOT / "roadmap/JOB_READY_CHECKLIST.pdf",
    ]
    paths.extend(ROOT / f"weeks/week-{week:02d}/WEEK_PLAN.pdf" for week in range(1, 25))
    for directory in ("project-01-tool-calling", "project-02-rag-knowledge-base", "project-03-agent-workflow", "project-04-capstone"):
        paths.extend([ROOT / f"projects/{directory}/REQUIREMENTS.pdf", ROOT / f"projects/{directory}/ARCHITECTURE.pdf"])
    return paths


def validate_yaml(path: Path) -> str | None:
    try:
        import yaml  # type: ignore
    except ImportError:
        # Simple syntax contract for generated YAML if PyYAML has not been installed yet.
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.strip() and not line.lstrip().startswith("#") and ":" not in line and not line.lstrip().startswith("-"):
                return f"invalid generated YAML syntax at line {number}"
        return None
    try:
        yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as error:  # noqa: BLE001
        return str(error)
    return None


def check_relative_markdown_links(path: Path) -> list[str]:
    failures: list[str] = []
    text = path.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        clean = target.split("#", 1)[0]
        if clean and not (path.parent / clean).exists():
            failures.append(f"{path.relative_to(ROOT)} -> {target}")
    return failures


def check_pdf(path: Path) -> str | None:
    if not path.exists() or path.stat().st_size < 500:
        return "missing_or_too_small"
    if shutil.which("pdftotext") is None:
        return None
    result = subprocess.run(["pdftotext", str(path), "-"], text=True, capture_output=True, check=False)
    if result.returncode != 0 or not result.stdout.strip():
        return "unreadable_or_empty_text"
    if not re.search(r"[\u4e00-\u9fff]", result.stdout):
        return "no_detectable_chinese_text"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Check generated learning-system files.")
    parser.add_argument("--require-pdfs", action="store_true", help="Treat missing PDFs as errors, not warnings.")
    args = parser.parse_args()
    errors: list[str] = []
    warnings: list[str] = []

    for relative in REQUIRED_ROOT:
        if not (ROOT / relative).exists():
            errors.append(f"missing: {relative}")
    for week in range(1, 25):
        prefix = ROOT / f"weeks/week-{week:02d}"
        for rel in ("README.md", "WEEK_PLAN.md", "CHECKLIST.md", "REVIEW.md", "resources/README.md", "notes/README.md", "exercises/README.md"):
            if not (prefix / rel).exists():
                errors.append(f"missing: {prefix.relative_to(ROOT) / rel}")
        for day in range(1, 8):
            if not (prefix / "days" / f"day-{day:02d}.md").exists():
                errors.append(f"missing: weeks/week-{week:02d}/days/day-{day:02d}.md")
    for directory in ("plan-a-foundation", "plan-b-job-ready", "plan-c-designer-ai"):
        for file in ("README.md", "CURRICULUM.md", "WEEKLY_SCHEDULE.md"):
            if not (ROOT / "plans" / directory / file).exists():
                errors.append(f"missing: plans/{directory}/{file}")
    for directory in ("project-01-tool-calling", "project-02-rag-knowledge-base", "project-03-agent-workflow", "project-04-capstone"):
        base = ROOT / "projects" / directory
        for file in ("README.md", "REQUIREMENTS.md", "ARCHITECTURE.md", "TASKS.md", "ACCEPTANCE_CRITERIA.md", "TEST_PLAN.md", "SECURITY.md", "EVALUATION.md", "DEPLOYMENT.md", "CHANGELOG.md", ".env.example", "pyproject.toml", "docker-compose.yml", "src/main.py", "tests/test_smoke.py"):
            if not (base / file).exists():
                errors.append(f"missing: projects/{directory}/{file}")

    for path in ROOT.rglob("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            errors.append(f"invalid JSON: {path.relative_to(ROOT)}: {error}")
    for path in list((ROOT / "config").glob("*.yaml")):
        yaml_error = validate_yaml(path)
        if yaml_error:
            errors.append(f"invalid YAML: {path.relative_to(ROOT)}: {yaml_error}")
    for path in ROOT.rglob("*.py"):
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as error:
            errors.append(f"invalid Python: {path.relative_to(ROOT)}:{error.lineno}: {error.msg}")
    for path in ROOT.rglob("*.md"):
        errors.extend(f"broken local Markdown link: {entry}" for entry in check_relative_markdown_links(path))
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".backups" in path.parts or path.suffix in {".pdf", ".pyc"}:
            continue
        if path.name == ".env.example":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"possible secret pattern: {path.relative_to(ROOT)}")
                break

    for path in required_pdfs():
        issue = check_pdf(path)
        if issue:
            target = errors if args.require_pdfs else warnings
            target.append(f"PDF {issue}: {path.relative_to(ROOT)}")

    report: dict[str, Any] = {"root": str(ROOT), "errors": errors, "warnings": warnings, "checked_markdown": len(list(ROOT.rglob('*.md'))), "checked_python": len(list(ROOT.rglob('*.py'))), "required_pdf_count": len(required_pdfs())}
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Validation: {len(errors)} error(s), {len(warnings)} warning(s). Report: {REPORT.relative_to(ROOT)}")
    for issue in errors[:20]:
        print(f"ERROR: {issue}")
    for issue in warnings[:20]:
        print(f"WARNING: {issue}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
