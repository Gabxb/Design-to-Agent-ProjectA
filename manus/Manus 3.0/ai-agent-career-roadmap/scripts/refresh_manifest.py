#!/usr/bin/env python3
"""Refresh config/file_manifest.json for the complete book-first tutorial."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    stamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    files = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or any(part in path.parts for part in {".pdf-build", ".book-pdf-build", ".backups", "__pycache__"}):
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel == "config/file_manifest.json":
            continue
        role = "supporting"
        if rel.startswith("book/part-") and "/chapter-" in rel:
            role = "canonical_tutorial_chapter"
        elif rel.startswith("weeks/"):
            role = "execution_plan"
        elif rel.startswith("projects/"):
            role = "portfolio_project"
        elif rel.startswith("overview/"):
            role = "global_overview"
        elif rel.startswith("knowledge-base/"):
            role = "reference_knowledge_base"
        elif rel.startswith("output/"):
            role = "generated_output"
        match_chapter = re.search(r"chapter-(\d+)-", rel)
        match_part = re.search(r"part-(\d+)-", rel)
        match_week = re.search(r"week-(\d+)", rel)
        project = rel.split("/")[1] if rel.startswith("projects/") and len(rel.split("/")) > 1 else None
        files.append({
            "path": rel,
            "file_type": path.suffix.lstrip(".") or "no_extension",
            "content_role": role,
            "part": int(match_part.group(1)) if match_part else None,
            "chapter": int(match_chapter.group(1)) if match_chapter else None,
            "plan": "plan-c-designer-ai" if role in {"canonical_tutorial_chapter", "execution_plan", "global_overview"} else None,
            "week": int(match_week.group(1)) if match_week else None,
            "project": project,
            "created_at": stamp,
            "last_updated": stamp,
            "contains_user_content": False,
            "needs_regeneration": path.suffix.lower() in {".pdf", ".html", ".png", ".svg"},
        })
    manifest = {"schema_version": 2, "generated_at": stamp, "canonical_source": "book/part-*/chapter-*.md", "files": files}
    target = ROOT / "config/file_manifest.json"
    target.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Manifest refreshed: {len(files)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
