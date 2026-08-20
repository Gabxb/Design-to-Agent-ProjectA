#!/usr/bin/env python3
"""Safely update learning progress without overwriting notes.

Every mutation creates a backup of progress and configuration files and appends a
human-readable entry to CHANGELOG.md. Run `python update_plan.py --help`.
"""
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
PROGRESS_PATH = ROOT / "progress/progress.json"
CURRENT_PLAN_PATH = ROOT / "config/current_plan.yaml"
CHANGELOG_PATH = ROOT / "CHANGELOG.md"
BACKUP_DIR = ROOT / ".backups"
VALID_PLANS = {"plan-a-foundation", "plan-b-job-ready", "plan-c-designer-ai"}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def load_progress() -> dict[str, Any]:
    if not PROGRESS_PATH.exists():
        raise FileNotFoundError("Missing progress/progress.json. Run python generate_files.py first.")
    return json.loads(PROGRESS_PATH.read_text(encoding="utf-8"))


def save_progress(progress: dict[str, Any]) -> None:
    progress["last_updated"] = now()
    PROGRESS_PATH.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def backup(reason: str) -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    target = BACKUP_DIR / f"{stamp}-{reason}"
    target.mkdir(parents=True, exist_ok=False)
    for rel in ("progress/progress.json", "progress/DAILY_LOG.md", "progress/WEEKLY_STATUS.md", "progress/SKILL_PROGRESS.md", "progress/PROBLEMS.md", "progress/COMPLETED_TASKS.md", "config/current_plan.yaml"):
        source = ROOT / rel
        if source.exists():
            destination = target / rel
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
    return target


def append_changelog(action: str, affected: list[str], details: str) -> None:
    entry = f"\n## {today()}\n\n### Changed\n- {action}: {details}\n\n### Affected Files\n" + "".join(f"- {item}\n" for item in affected)
    with CHANGELOG_PATH.open("a", encoding="utf-8") as file:
        file.write(entry)


def append_markdown(relative: str, text: str) -> None:
    with (ROOT / relative).open("a", encoding="utf-8") as file:
        file.write(text if text.endswith("\n") else text + "\n")


def write_current_plan(plan: str, progress: dict[str, Any], status: str = "active") -> None:
    names = {
        "plan-a-foundation": "方案 A：稳健基础版",
        "plan-b-job-ready": "方案 B：求职冲刺版",
        "plan-c-designer-ai": "方案 C：设计师优势版",
    }
    content = (
        f"current_plan: {plan}\n"
        f"plan_name: {names[plan]}\n"
        f"current_week: {progress['current_week']}\n"
        f"current_day: {progress['current_day']}\n"
        f"status: {status}\n"
        f"last_updated: {today()}\n"
    )
    CURRENT_PLAN_PATH.write_text(content, encoding="utf-8")


def cmd_status(_: argparse.Namespace) -> int:
    progress = load_progress()
    print(json.dumps({
        "current_plan": progress["current_plan"],
        "current_week": progress["current_week"],
        "current_day": progress["current_day"],
        "learning_hours": progress["learning_hours"],
        "completed_task_count": len(progress["completed_tasks"]),
        "status": progress.get("status", "active"),
        "last_updated": progress["last_updated"],
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_set_position(args: argparse.Namespace) -> int:
    if not 1 <= args.week <= 24 or not 1 <= args.day <= 7:
        raise ValueError("week must be 1–24 and day must be 1–7")
    backup("set-position")
    progress = load_progress()
    progress["current_week"] = args.week
    progress["current_day"] = args.day
    save_progress(progress)
    write_current_plan(progress["current_plan"], progress, progress.get("status", "active"))
    append_changelog("Updated current position", ["progress/progress.json", "config/current_plan.yaml"], f"Moved to week {args.week:02d}, day {args.day:02d}.")
    print(f"Current position: week {args.week:02d}, day {args.day:02d}")
    return 0


def cmd_complete(args: argparse.Namespace) -> int:
    backup("complete-task")
    progress = load_progress()
    task = args.task.strip()
    if not task:
        raise ValueError("task must not be empty")
    if task not in progress["completed_tasks"]:
        progress["completed_tasks"].append(task)
    save_progress(progress)
    append_markdown("progress/COMPLETED_TASKS.md", f"- [x] {task} — {today()}")
    append_changelog("Completed task", ["progress/progress.json", "progress/COMPLETED_TASKS.md"], task)
    print(f"Completed: {task}")
    return 0


def cmd_hours(args: argparse.Namespace) -> int:
    if args.value <= 0:
        raise ValueError("hours value must be greater than zero")
    backup("add-hours")
    progress = load_progress()
    progress["learning_hours"] = round(float(progress["learning_hours"]) + args.value, 2)
    save_progress(progress)
    append_markdown("progress/DAILY_LOG.md", f"| {today()} | week-{progress['current_week']:02d}/day-{progress['current_day']:02d} | {args.value:g} | 学习时长已记录 |  |  |")
    append_changelog("Added learning hours", ["progress/progress.json", "progress/DAILY_LOG.md"], f"+{args.value:g} hours")
    print(f"Total learning hours: {progress['learning_hours']}")
    return 0


def cmd_problem(args: argparse.Namespace) -> int:
    backup("add-problem")
    progress = load_progress()
    item = {"date": today(), "text": args.text, "status": "open"}
    progress["problems"].append(item)
    save_progress(progress)
    safe_text = args.text.replace("|", "\\|").replace("\n", " ")
    append_markdown("progress/PROBLEMS.md", f"| {today()} | {safe_text} | 待补充 | 待补充 | 复现并缩小范围 | open |")
    append_changelog("Added problem", ["progress/progress.json", "progress/PROBLEMS.md"], "Recorded a learning problem.")
    print("Problem recorded.")
    return 0


def cmd_note(args: argparse.Namespace) -> int:
    backup("add-note")
    progress = load_progress()
    item = {"date": today(), "text": args.text}
    progress["custom_notes"].append(item)
    save_progress(progress)
    append_markdown("progress/DAILY_LOG.md", f"\n> {today()} 个人笔记：{args.text}\n")
    append_changelog("Added personal note", ["progress/progress.json", "progress/DAILY_LOG.md"], "Personal note preserved.")
    print("Personal note recorded.")
    return 0


def cmd_switch_plan(args: argparse.Namespace) -> int:
    plan = args.plan
    if plan not in VALID_PLANS:
        raise ValueError(f"plan must be one of: {', '.join(sorted(VALID_PLANS))}")
    backup("switch-plan")
    progress = load_progress()
    previous = progress["current_plan"]
    progress["current_plan"] = plan
    save_progress(progress)
    write_current_plan(plan, progress, progress.get("status", "active"))
    migration = ROOT / "plans" / f"MIGRATION_{previous}_TO_{plan}_{today()}.md"
    migration.write_text(
        f"# 学习方案迁移说明\n\n- 原方案：`{previous}`\n- 新方案：`{plan}`\n- 迁移日期：{today()}\n- 当前进度：Week {progress['current_week']:02d} / Day {progress['current_day']:02d}\n\n已完成任务和个人笔记保留；仅重新安排当前周之后尚未完成的任务。请查看新方案目录中的 `WEEKLY_SCHEDULE.md`，并从当前周的未完成 Day 开始。\n",
        encoding="utf-8",
    )
    append_changelog("Switched learning plan", ["progress/progress.json", "config/current_plan.yaml", str(migration.relative_to(ROOT))], f"{previous} -> {plan}; completed work retained.")
    print(f"Switched from {previous} to {plan}. Migration note: {migration.relative_to(ROOT)}")
    return 0


def cmd_pause(args: argparse.Namespace) -> int:
    backup("pause")
    progress = load_progress()
    progress["status"] = "paused"
    progress["paused_at"] = now()
    progress["pause_reason"] = args.reason
    save_progress(progress)
    write_current_plan(progress["current_plan"], progress, "paused")
    recovery = ROOT / "progress/RECOVERY_CHECKLIST.md"
    recovery.write_text(
        f"# 恢复学习清单\n\n暂停时间：{progress['paused_at']}\n\n暂停原因：{args.reason}\n\n恢复时按以下顺序：\n\n- [ ] 阅读 `progress/progress.json`，确认当前周/日与未完成任务。\n- [ ] 重跑当前项目的最小测试或示例。\n- [ ] 阅读当前日任务和上一条每日学习日志。\n- [ ] 用 30 分钟完成一个小复习，再使用 `python update_plan.py resume`。\n\n原任务未删除。\n",
        encoding="utf-8",
    )
    append_changelog("Paused learning", ["progress/progress.json", "config/current_plan.yaml", "progress/RECOVERY_CHECKLIST.md"], args.reason)
    print("Learning paused; recovery checklist created.")
    return 0


def cmd_resume(_: argparse.Namespace) -> int:
    backup("resume")
    progress = load_progress()
    progress["status"] = "active"
    resumed_from = progress.get("paused_at")
    progress["paused_at"] = None
    save_progress(progress)
    write_current_plan(progress["current_plan"], progress, "active")
    recovery = ROOT / "progress/RECOVERY_PLAN.md"
    recovery.write_text(
        f"# 恢复学习计划\n\n恢复日期：{today()}\n\n从暂停记录恢复：{resumed_from or '未记录'}。当前起点为 Week {progress['current_week']:02d} / Day {progress['current_day']:02d}。\n\n1. 用 30 分钟阅读当前周 `WEEK_PLAN.md` 和上一次 `DAILY_LOG.md` 条目。\n2. 用 30–60 分钟运行一个最小样例或测试，确认环境仍然可用。\n3. 先完成当前日未完成的最小验收；扩展项可移至 Day 7。\n4. 更新 `progress/DAILY_LOG.md`，再继续后续日程。\n\n未完成任务没有被删除；请根据 `progress.json` 的 completed_tasks 自行核对。\n",
        encoding="utf-8",
    )
    append_changelog("Resumed learning", ["progress/progress.json", "config/current_plan.yaml", "progress/RECOVERY_PLAN.md"], "Created a short recovery plan and kept incomplete tasks.")
    print("Learning resumed; recovery plan created.")
    return 0


def cmd_regenerate(args: argparse.Namespace) -> int:
    if not 1 <= args.from_week <= 24:
        raise ValueError("from-week must be 1–24")
    backup("regenerate-plan")
    progress = load_progress()
    report = ROOT / "plans" / f"REGENERATION_FROM_WEEK_{args.from_week:02d}_{today()}.md"
    report.write_text(
        f"# 后续计划重生成记录\n\n本次请求从 Week {args.from_week:02d} 开始重新规划。当前方案：`{progress['current_plan']}`；已完成任务数：{len(progress['completed_tasks'])}。\n\n为保护个人笔记，默认生成器不会覆盖已有的 `notes/`、`progress/` 或项目文档。请先复制需改写的周计划为 `WEEK_PLAN.v2.md`，再根据新约束修改；保留旧文件作为历史版本。\n\n建议命令：`python generate_files.py` 用于补齐缺失文件；不要使用 `--force` 覆盖个人文件。\n",
        encoding="utf-8",
    )
    append_changelog("Requested future-plan regeneration", [str(report.relative_to(ROOT))], f"from week {args.from_week:02d}; existing notes preserved.")
    print(f"Regeneration record created: {report.relative_to(ROOT)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Maintain AI Agent learning progress safely.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("status", help="Show current progress.").set_defaults(func=cmd_status)
    position = subparsers.add_parser("set-position", help="Update current week and day.")
    position.add_argument("--week", type=int, required=True)
    position.add_argument("--day", type=int, required=True)
    position.set_defaults(func=cmd_set_position)
    complete = subparsers.add_parser("complete", help="Mark a task completed.")
    complete.add_argument("--task", required=True)
    complete.set_defaults(func=cmd_complete)
    hours = subparsers.add_parser("hours", help="Add learning time.")
    hours.add_argument("--value", type=float, required=True)
    hours.set_defaults(func=cmd_hours)
    problem = subparsers.add_parser("problem", help="Record a learning problem.")
    problem.add_argument("--text", required=True)
    problem.set_defaults(func=cmd_problem)
    note = subparsers.add_parser("note", help="Record a personal note.")
    note.add_argument("--text", required=True)
    note.set_defaults(func=cmd_note)
    switch = subparsers.add_parser("switch-plan", help="Switch plan and preserve completed work.")
    switch.add_argument("plan", choices=sorted(VALID_PLANS))
    switch.set_defaults(func=cmd_switch_plan)
    pause = subparsers.add_parser("pause", help="Pause study and create recovery checklist.")
    pause.add_argument("--reason", required=True)
    pause.set_defaults(func=cmd_pause)
    subparsers.add_parser("resume", help="Resume study and create short recovery plan.").set_defaults(func=cmd_resume)
    regenerate = subparsers.add_parser("regenerate", help="Create a safe future-plan regeneration record.")
    regenerate.add_argument("--from-week", type=int, required=True)
    regenerate.set_defaults(func=cmd_regenerate)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return args.func(args)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
