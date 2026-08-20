#!/usr/bin/env python3
"""Create output-level generation, validation and file-list reports."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    all_files = sorted(
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file() and not any(part in path.parts for part in {".pdf-build", ".book-pdf-build", ".backups", "__pycache__"})
    )
    (OUT / "file-list.txt").write_text("\n".join(all_files) + "\n", encoding="utf-8")
    validation_path = ROOT / "reports/tutorial_validation_report.json"
    if not validation_path.exists():
        validation_path = ROOT / "reports/validation_report.json"
    validation = {"errors": [], "warnings": ["Validation has not been run yet."]}
    if validation_path.exists():
        validation = json.loads(validation_path.read_text(encoding="utf-8"))
    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    (OUT / "GENERATION_REPORT.md").write_text(
        f"# 文件生成报告\n\n- 生成时间：{generated}\n- 书籍名称：《从设计师到 AI Agent 开发工程师：24 周本地实战教程》\n- 默认方案：方案 C：设计师优势版\n- 文件总数：{len(all_files)}\n- 全书入口：`BOOK.md`\n- 输出书籍：`output/book/ai-agent-career-roadmap.md`、`.html`、`.pdf`\n- 一页总览：`overview/ONE_PAGE_OVERVIEW.md`\n- 学习地图：`overview/LEARNING_MAP.md`\n- 第一天任务：`weeks/week-01/days/day-01.md`\n",
        encoding="utf-8",
    )
    (OUT / "VALIDATION_REPORT.md").write_text(
        "# 文件验证报告\n\n"
        f"- 错误数：{len(validation.get('errors', []))}\n"
        f"- 警告数：{len(validation.get('warnings', []))}\n\n"
        "## 错误\n\n" + ("\n".join(f"- {item}" for item in validation.get("errors", [])) or "- 无。")
        + "\n\n## 警告\n\n" + ("\n".join(f"- {item}" for item in validation.get("warnings", [])) or "- 无。") + "\n",
        encoding="utf-8",
    )
    print(f"Output reports written for {len(all_files)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
