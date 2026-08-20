#!/usr/bin/env python3
"""Render trusted Mermaid tutorial sources to SVG and PNG."""
from __future__ import annotations

import base64
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def source_files() -> list[Path]:
    files = list((ROOT / "overview").glob("*.mmd"))
    files.extend((ROOT / "plans").glob("plan-*/ROADMAP.mmd"))
    files.extend(ROOT / f"weeks/week-{week:02d}/MINDMAP.mmd" for week in range(1, 25))
    for project in ("project-01-tool-calling", "project-02-rag-knowledge-base", "project-03-agent-workflow", "project-04-capstone"):
        files.extend([ROOT / "projects" / project / "ARCHITECTURE.mmd", ROOT / "projects" / project / "AGENT_WORKFLOW.mmd"])
    return [path for path in files if path.exists()]


def render(source: Path, target: Path) -> bool:
    # The local renderer produces PNG. Mermaid remains the editable primary source;
    # SVG is a standards-compliant image wrapper generated from that rendered PNG.
    png_target = target if target.suffix == ".png" else target.with_suffix(".svg-source.png")
    result = subprocess.run(["manus-render-diagram", str(source), str(png_target)], cwd=ROOT, text=True, capture_output=True, check=False)
    actual_png = png_target if png_target.exists() else Path(str(png_target) + ".png")
    if result.returncode != 0 or not actual_png.exists() or actual_png.stat().st_size <= 100:
        print(f"FAIL {source.relative_to(ROOT)} -> {target.relative_to(ROOT)}", file=sys.stderr)
        print(result.stderr[-800:], file=sys.stderr)
        return False
    if target.suffix == ".svg":
        encoded = base64.b64encode(actual_png.read_bytes()).decode("ascii")
        target.write_text(
            "<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" viewBox=\"0 0 3120 1800\">"
            f"<image width=\"3120\" height=\"1800\" xlink:href=\"data:image/png;base64,{encoded}\"/>"
            "</svg>\n",
            encoding="utf-8",
        )
        if actual_png != target.with_suffix(".png"):
            actual_png.unlink(missing_ok=True)
    return target.exists() and target.stat().st_size > 100


def main() -> int:
    sources = source_files()
    failures: list[str] = []
    successes = 0
    for source in sources:
        for suffix in (".svg", ".png"):
            target = source.with_suffix(suffix)
            if render(source, target):
                successes += 1
            else:
                failures.append(source.relative_to(ROOT).as_posix())
    print(f"Mindmap render complete: {successes} artifacts, {len(failures)} failures.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
