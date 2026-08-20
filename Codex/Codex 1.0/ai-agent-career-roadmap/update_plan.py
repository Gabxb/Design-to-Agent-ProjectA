#!/usr/bin/env python3
"""Backup-first progress and plan management for the learning system."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROGRESS = ROOT / "progress/progress.json"
CHANGELOG = ROOT / "CHANGELOG.md"
VALID_PLANS = {"plan-a-foundation", "plan-b-job-ready", "plan-c-designer-ai"}


def backup() -> Path:
    stamp = datetime.now().strftime("%Y-%m-%d-%H%M%S-%f")
    target = ROOT / "backups" / stamp
    target.mkdir(parents=True, exist_ok=False)
    for relative in ("progress", "config/current_plan.yaml", "CHANGELOG.md"):
        source = ROOT / relative
        destination = target / relative
        if source.is_dir():
            shutil.copytree(source, destination)
        elif source.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
    return target


def load_progress() -> dict[str, object]:
    return json.loads(PROGRESS.read_text(encoding="utf-8"))


def save_progress(data: dict[str, object]) -> None:
    data["last_updated"] = datetime.now().isoformat(timespec="seconds")
    temp = PROGRESS.with_suffix(".json.tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(PROGRESS)


def append_changelog(action: str, affected: list[str]) -> None:
    entry = f"""
## {date.today().isoformat()}

### Added
- 自动备份本次更新前的学习状态。

### Changed
- {action}

### Fixed
- 保留已完成任务、学习时间、问题和个人笔记。

### Affected Files
{''.join(f'- {item}{chr(10)}' for item in affected)}
"""
    with CHANGELOG.open("a", encoding="utf-8") as stream:
        stream.write(entry)


def write_current_plan(plan: str, current_week: int) -> None:
    content = f"""plan: {plan}
plan_week: {current_week}
source_curriculum_week: {current_week}
status: active
selected_at: {date.today().isoformat()}
migration_note: "由 update_plan.py 更新；原进度已备份。"
"""
    (ROOT / "config/current_plan.yaml").write_text(content, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="更新学习进度、暂停/恢复或切换方案")
    sub = parser.add_subparsers(dest="command", required=True)
    set_day = sub.add_parser("set-day", help="更新当前周和天")
    set_day.add_argument("week", type=int)
    set_day.add_argument("day", type=int)
    complete = sub.add_parser("complete", help="标记任务完成")
    complete.add_argument("task_id")
    hours = sub.add_parser("add-hours", help="添加学习时间")
    hours.add_argument("hours", type=float)
    problem = sub.add_parser("add-problem", help="添加问题")
    problem.add_argument("text")
    note = sub.add_parser("add-note", help="添加个人笔记")
    note.add_argument("text")
    switch = sub.add_parser("switch-plan", help="切换学习方案")
    switch.add_argument("plan", choices=sorted(VALID_PLANS))
    intensity = sub.add_parser("set-intensity", help="调整每周学习时长并记录后续重排建议")
    intensity.add_argument("hours", type=float)
    pause = sub.add_parser("pause", help="暂停学习")
    pause.add_argument("--reason", default="未填写原因")
    sub.add_parser("resume", help="恢复学习并生成复习清单")
    sub.add_parser("regenerate", help="重新生成后续计划；保留学习者文件")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    backup_path = backup()
    data = load_progress()
    action = ""
    affected = ["progress/progress.json", "CHANGELOG.md"]

    if args.command == "set-day":
        if not 1 <= args.week <= 24 or not 1 <= args.day <= 7:
            raise SystemExit("week 必须为 1-24，day 必须为 1-7")
        data["current_week"], data["current_day"] = args.week, args.day
        action = f"当前学习位置更新为 Week {args.week:02d} Day {args.day:02d}。"
    elif args.command == "complete":
        completed = data.setdefault("completed_tasks", [])
        if args.task_id not in completed:
            completed.append(args.task_id)
            with (ROOT / "progress/COMPLETED_TASKS.md").open("a", encoding="utf-8") as stream:
                stream.write(f"\n- [x] {args.task_id} — {date.today().isoformat()}\n")
        action = f"任务 {args.task_id} 标记为完成。"
        affected.append("progress/COMPLETED_TASKS.md")
    elif args.command == "add-hours":
        if args.hours <= 0:
            raise SystemExit("学习时间必须大于 0")
        data["learning_hours"] = round(float(data.get("learning_hours", 0)) + args.hours, 2)
        action = f"增加学习时间 {args.hours} 小时。"
    elif args.command == "add-problem":
        item = {"date": date.today().isoformat(), "text": args.text, "status": "open"}
        data.setdefault("problems", []).append(item)
        with (ROOT / "progress/PROBLEMS.md").open("a", encoding="utf-8") as stream:
            stream.write(f"\n## {date.today().isoformat()}\n\n- {args.text}\n")
        action = "新增学习问题。"
        affected.append("progress/PROBLEMS.md")
    elif args.command == "add-note":
        data.setdefault("custom_notes", []).append({"date": date.today().isoformat(), "text": args.text})
        with (ROOT / "progress/DAILY_LOG.md").open("a", encoding="utf-8") as stream:
            stream.write(f"\n## {date.today().isoformat()}\n\n- {args.text}\n")
        action = "新增个人学习笔记。"
        affected.append("progress/DAILY_LOG.md")
    elif args.command == "switch-plan":
        old = str(data.get("current_plan"))
        data["current_plan"] = args.plan
        data.setdefault("plan_history", []).append({"date": date.today().isoformat(), "from": old, "to": args.plan})
        migration = ROOT / "progress" / f"PLAN_MIGRATION_{date.today().isoformat()}.md"
        migration.write_text(f"# 方案迁移说明\n\n- 原方案：{old}\n- 新方案：{args.plan}\n- 当前源课程周：{data.get('current_week', 1)}\n- 已完成任务：{len(data.get('completed_tasks', []))}\n- 迁移原则：复用完成内容，只重新安排未完成任务。\n", encoding="utf-8")
        write_current_plan(args.plan, int(data.get("current_week", 1)))
        action = f"学习方案从 {old} 切换为 {args.plan}。"
        affected += ["config/current_plan.yaml", migration.relative_to(ROOT).as_posix()]
    elif args.command == "set-intensity":
        if not 5 <= args.hours <= 40:
            raise SystemExit("每周时长建议在 5-40 小时之间")
        data["weekly_hours"] = args.hours
        data["reschedule_note"] = f"从 Week {data.get('current_week', 1)} 起按每周 {args.hours} 小时重新分配未完成任务；已完成任务不移动。"
        action = f"每周学习强度调整为 {args.hours} 小时。"
    elif args.command == "pause":
        data["status"] = "paused"
        data["paused_at"] = date.today().isoformat()
        data["pause_reason"] = args.reason
        resume = ROOT / "progress/RESUME_CHECKLIST.md"
        resume.write_text("# 恢复学习清单\n\n- [ ] 阅读暂停前一周 REVIEW\n- [ ] 重跑最后一个成功命令\n- [ ] 复习三个核心概念\n- [ ] 完成一个 30 分钟最小任务\n- [ ] 重新安排未完成任务，不删除原任务\n", encoding="utf-8")
        action = f"学习已暂停，原因：{args.reason}。"
        affected.append("progress/RESUME_CHECKLIST.md")
    elif args.command == "resume":
        data["status"] = "active"
        data["resumed_at"] = date.today().isoformat()
        data["resume_plan"] = ["阅读最近周复盘", "重跑最后成功案例", "复习核心概念", "完成一个小任务", "重排未完成内容"]
        action = "学习已恢复，并生成简短复习与重新排期清单。"
    elif args.command == "regenerate":
        completed_before = list(data.get("completed_tasks", []))
        notes_before = list(data.get("custom_notes", []))
        subprocess.run([sys.executable, str(ROOT / "generate_files.py")], cwd=ROOT, check=True)
        data = load_progress()
        data["completed_tasks"] = completed_before
        data["custom_notes"] = notes_before
        action = "重新生成学习文件，并保留已完成任务与个人笔记。"
        affected.append("config/file_manifest.json")

    save_progress(data)
    append_changelog(action, affected)
    print(f"{action}\n备份：{backup_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
