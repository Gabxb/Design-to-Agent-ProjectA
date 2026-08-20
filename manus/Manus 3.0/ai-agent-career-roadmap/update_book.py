#!/usr/bin/env python3
"""Safely maintain book-reading progress while preserving user notes and backups."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
PROGRESS = ROOT / "progress/progress.json"
BACKUPS = ROOT / ".backups"
CHANGELOG = ROOT / "CHANGELOG.md"
VALID_PLANS = {"plan-a-foundation", "plan-b-job-ready", "plan-c-designer-ai"}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def load() -> dict[str, Any]:
    return json.loads(PROGRESS.read_text(encoding="utf-8"))


def save(data: dict[str, Any]) -> None:
    data["last_updated"] = now()
    PROGRESS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def backup(reason: str) -> Path:
    target = BACKUPS / f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-{reason}"
    for relative in ("progress", "config/current_plan.yaml", "CHANGELOG.md"):
        source = ROOT / relative
        if source.exists():
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, destination, dirs_exist_ok=True)
            else:
                shutil.copy2(source, destination)
    return target


def changelog(action: str, files: list[str]) -> None:
    with CHANGELOG.open("a", encoding="utf-8") as handle:
        handle.write(f"\n## {today()}\n\n### Changed\n- {action}\n\n### Affected Files\n" + "".join(f"- {file}\n" for file in files))


def cmd_status(_: argparse.Namespace) -> int:
    data = load()
    fields = {key: data.get(key) for key in ("current_plan", "current_part", "current_chapter", "current_week", "current_day", "learning_hours", "paused_at")}
    fields["completed_task_count"] = len(data.get("completed_tasks", []))
    fields["completed_chapter_count"] = len(data.get("completed_chapters", []))
    print(json.dumps(fields, ensure_ascii=False, indent=2))
    return 0


def cmd_position(args: argparse.Namespace) -> int:
    if not 1 <= args.part <= 8 or not 1 <= args.chapter <= 70 or not 1 <= args.week <= 24 or not 1 <= args.day <= 7:
        raise ValueError("part 1–8, chapter 1–70, week 1–24, day 1–7 are required")
    backup("book-position")
    data = load()
    data.update({"current_part": args.part, "current_chapter": args.chapter, "current_week": args.week, "current_day": args.day, "paused_at": None})
    save(data)
    changelog(f"Updated book position to part {args.part}, chapter {args.chapter}, week {args.week}, day {args.day}.", ["progress/progress.json"])
    return 0


def cmd_complete_chapter(args: argparse.Namespace) -> int:
    if not 1 <= args.chapter <= 70:
        raise ValueError("chapter must be 1–70")
    backup("complete-chapter")
    data = load()
    completed = data.setdefault("completed_chapters", [])
    if args.chapter not in completed:
        completed.append(args.chapter)
        completed.sort()
    save(data)
    with (ROOT / "progress/COMPLETED_TASKS.md").open("a", encoding="utf-8") as handle:
        handle.write(f"- [x] chapter-{args.chapter:02d} — {today()}\n")
    changelog(f"Completed chapter {args.chapter}.", ["progress/progress.json", "progress/COMPLETED_TASKS.md"])
    return 0


def cmd_complete_task(args: argparse.Namespace) -> int:
    backup("complete-book-task")
    return subprocess.run([sys.executable, str(ROOT / "update_plan.py"), "complete", "--task", args.task], cwd=ROOT, check=False).returncode


def cmd_problem(args: argparse.Namespace) -> int:
    backup("book-problem")
    return subprocess.run([sys.executable, str(ROOT / "update_plan.py"), "problem", "--text", args.text], cwd=ROOT, check=False).returncode


def cmd_intensity(args: argparse.Namespace) -> int:
    if args.hours < 1 or args.hours > 40:
        raise ValueError("hours must be between 1 and 40")
    backup("adjust-intensity")
    data = load()
    note = ROOT / f"plans/INTENSITY_ADJUSTMENT_{today()}.md"
    note.write_text(
        f"# 学习强度调整记录\\n\\n新的每周目标：{args.hours:g} 小时。\\n\\n从 Week {data.get('current_week', 1):02d} / Day {data.get('current_day', 1):02d} 开始，仅重新分配未完成任务；已完成任务、章节和个人笔记保持不变。优先保留每天的最小可验证闭环：阅读核心章节、运行最小示例、完成一个验证、更新日志。扩展任务移至 Day 7 或后续补做区。\\n",
        encoding="utf-8",
    )
    changelog(f"Adjusted future learning intensity to {args.hours:g} hours per week.", [note.relative_to(ROOT).as_posix()])
    return 0


def cmd_project(args: argparse.Namespace) -> int:
    backup("project-progress")
    data = load()
    data.setdefault("project_progress", {})[args.project] = {"status": args.status, "updated_at": now()}
    save(data)
    changelog(f"Updated project progress: {args.project} -> {args.status}.", ["progress/progress.json"])
    return 0


def cmd_hours(args: argparse.Namespace) -> int:
    if args.value <= 0:
        raise ValueError("hours must be positive")
    backup("book-hours")
    data = load()
    data["learning_hours"] = round(float(data.get("learning_hours", 0)) + args.value, 2)
    save(data)
    changelog(f"Added {args.value:g} learning hours.", ["progress/progress.json"])
    return 0


def cmd_note(args: argparse.Namespace) -> int:
    backup("book-note")
    data = load()
    data.setdefault("custom_notes", []).append({"date": today(), "text": args.text})
    save(data)
    with (ROOT / "progress/DAILY_LOG.md").open("a", encoding="utf-8") as handle:
        handle.write(f"\n> {today()} 书籍笔记：{args.text}\n")
    changelog("Added personal book note; user content preserved.", ["progress/progress.json", "progress/DAILY_LOG.md"])
    return 0


def cmd_pause(args: argparse.Namespace) -> int:
    backup("book-pause")
    data = load()
    data["paused_at"] = now()
    data["pause_reason"] = args.reason
    save(data)
    (ROOT / "progress/BOOK_RECOVERY_CHECKLIST.md").write_text(
        f"# 恢复阅读清单\n\n暂停时间：{data['paused_at']}\n\n原因：{args.reason}\n\n- [ ] 阅读当前章节与最近一条每日日志。\n- [ ] 运行当前项目的最小测试或示例。\n- [ ] 用 30 分钟复习当前周核心概念。\n- [ ] 使用 `python update_book.py resume` 生成恢复计划。\n",
        encoding="utf-8",
    )
    changelog("Paused learning and created book recovery checklist.", ["progress/progress.json", "progress/BOOK_RECOVERY_CHECKLIST.md"])
    return 0


def cmd_resume(_: argparse.Namespace) -> int:
    backup("book-resume")
    data = load()
    old_pause = data.get("paused_at")
    data["paused_at"] = None
    save(data)
    (ROOT / "progress/BOOK_RECOVERY_PLAN.md").write_text(
        f"# 恢复学习计划\n\n从暂停记录恢复：{old_pause or '未记录'}。\n\n当前阅读位置：第 {data.get('current_part', 1)} 篇，第 {data.get('current_chapter', 1)} 章；Week {data.get('current_week', 1):02d} / Day {data.get('current_day', 1):02d}。\n\n1. 阅读当前章节的“本章总结”。\n2. 运行当前章节最小示例。\n3. 完成当天的最小任务与一项验收。\n4. 将扩展任务移动到 Day 7，不删除历史记录。\n",
        encoding="utf-8",
    )
    changelog("Resumed learning and created book recovery plan.", ["progress/progress.json", "progress/BOOK_RECOVERY_PLAN.md"])
    return 0


def cmd_switch(args: argparse.Namespace) -> int:
    backup("book-switch-plan")
    data = load()
    old = data.get("current_plan")
    data["current_plan"] = args.plan
    save(data)
    migration = ROOT / f"plans/BOOK_MIGRATION_{old}_TO_{args.plan}_{today()}.md"
    migration.write_text(
        f"# 书籍学习方案迁移\n\n原方案：`{old}`\n\n新方案：`{args.plan}`\n\n已完成章节、任务、项目证据和个人笔记保留。只重新安排当前 Week {data.get('current_week', 1):02d} 之后尚未完成的执行任务。\n",
        encoding="utf-8",
    )
    changelog(f"Switched book plan from {old} to {args.plan}; completed work preserved.", ["progress/progress.json", migration.relative_to(ROOT).as_posix()])
    return 0


def cmd_rebuild(args: argparse.Namespace) -> int:
    commands = {
        "toc": [sys.executable, str(ROOT / "scripts/upgrade_tutorial.py")],
        "mindmaps": [sys.executable, str(ROOT / "scripts/generate_mindmaps.py")],
        "book": [sys.executable, str(ROOT / "scripts/build_book.py")],
        "pdf": [sys.executable, str(ROOT / "scripts/build_book_pdf.py")],
    }
    result = subprocess.run(commands[args.target], cwd=ROOT, check=False)
    return result.returncode


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Maintain book-reading progress safely.")
    subs = root.add_subparsers(dest="command", required=True)
    subs.add_parser("status").set_defaults(func=cmd_status)
    pos = subs.add_parser("position")
    pos.add_argument("--part", type=int, required=True)
    pos.add_argument("--chapter", type=int, required=True)
    pos.add_argument("--week", type=int, required=True)
    pos.add_argument("--day", type=int, required=True)
    pos.set_defaults(func=cmd_position)
    chapter = subs.add_parser("complete-chapter")
    chapter.add_argument("--chapter", type=int, required=True)
    chapter.set_defaults(func=cmd_complete_chapter)
    task = subs.add_parser("complete-task")
    task.add_argument("--task", required=True)
    task.set_defaults(func=cmd_complete_task)
    problem = subs.add_parser("problem")
    problem.add_argument("--text", required=True)
    problem.set_defaults(func=cmd_problem)
    intensity = subs.add_parser("adjust-intensity")
    intensity.add_argument("--hours", type=float, required=True)
    intensity.set_defaults(func=cmd_intensity)
    project = subs.add_parser("project")
    project.add_argument("--project", required=True)
    project.add_argument("--status", required=True)
    project.set_defaults(func=cmd_project)
    hours = subs.add_parser("hours")
    hours.add_argument("--value", type=float, required=True)
    hours.set_defaults(func=cmd_hours)
    note = subs.add_parser("note")
    note.add_argument("--text", required=True)
    note.set_defaults(func=cmd_note)
    pause = subs.add_parser("pause")
    pause.add_argument("--reason", required=True)
    pause.set_defaults(func=cmd_pause)
    subs.add_parser("resume").set_defaults(func=cmd_resume)
    switch = subs.add_parser("switch-plan")
    switch.add_argument("plan", choices=sorted(VALID_PLANS))
    switch.set_defaults(func=cmd_switch)
    rebuild = subs.add_parser("rebuild")
    rebuild.add_argument("target", choices=["toc", "mindmaps", "book", "pdf"])
    rebuild.set_defaults(func=cmd_rebuild)
    return root


def main() -> int:
    try:
        args = parser().parse_args()
        return args.func(args)
    except (ValueError, FileNotFoundError, json.JSONDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
