#!/usr/bin/env python3
"""Create required roadmap and navigation artifacts for plans A, B and C."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PLANS = {
    "plan-a-foundation": ("方案 A：稳健基础版", "24 周，每周 10–15 小时", "强化 Python 与工程基础，适合在职且基础较弱的学习者。"),
    "plan-b-job-ready": ("方案 B：求职冲刺版", "16 周，每周 20–25 小时", "以每四周一个展示成果为节奏，快速形成项目与求职材料。"),
    "plan-c-designer-ai": ("方案 C：设计师优势版", "20 周核心 + 4 周求职冲刺，每周 15–20 小时", "将用户研究、信息架构、交互设计和 Human-in-the-loop 转化为工程优势。"),
}

STAGES = [
    ("基础", "Python、API、数据库、测试、Docker", "设计需求结构化助手 API"),
    ("LLM", "Prompt、Structured Output、Tool Calling", "UX Research Copilot"),
    ("RAG", "解析、检索、引用、评测、权限隔离", "设计规范知识库 Agent"),
    ("工作流", "状态、HITL、LangGraph、MCP", "智能设计评审 Agent"),
    ("生产化", "Evaluation、安全、Tracing、部署", "案例分流与合规助手"),
    ("求职", "GitHub、Demo、简历、面试、投递", "全作品集"),
]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    for directory, (name, duration, description) in PLANS.items():
        base = ROOT / "plans" / directory
        rows = []
        for index, (stage, tech, project) in enumerate(STAGES, 1):
            rows.append(f"| {index} | {stage} | {tech} | {project} |")
        roadmap = f"""# {name}：路线图

## 计划定位

{description}

| 属性 | 设置 |
|---|---|
| 学习周期与投入 | {duration} |
| 主要方向 | AI Agent 开发工程、AI 产品工程、设计技术/智能体验方向 |
| 默认切换原则 | 保留已完成任务和个人笔记，仅调整后续未完成任务。 |

## 阶段路径

| 阶段 | 名称 | 核心技术 | 阶段项目 |
|---:|---|---|---|
{chr(10).join(rows)}

## 使用方式

查看 `WEEK_INDEX.md` 确认该方案的节奏；查看 `PROJECT_PATH.md` 了解项目如何递进；查看 `RISKS.md` 提前处理时间、基础、范围与工程质量风险。
"""
        mmd = "flowchart LR\n" + "\n".join(f"  S{i}[{stage}\\n{project}]" for i, (stage, _, project) in enumerate(STAGES, 1)) + "\n" + "\n".join(f"  S{i} --> S{i+1}" for i in range(1, len(STAGES))) + "\n"
        weekly = "\n".join(f"| Week {week:02d} | 参照根目录 `weeks/week-{week:02d}/` 的执行计划；按本方案投入强度安排未完成任务。 |" for week in range(1, 25 if directory != "plan-b-job-ready" else 17))
        project_path = "\n".join(f"{idx}. **{project}：**{tech}。" for idx, (_, tech, project) in enumerate(STAGES, 1))
        risks = """# 学习风险与应对

| 风险 | 早期信号 | 应对方式 |
|---|---|---|
| 基础不稳 | 无法解释或修改最小示例 | 回到对应书籍章节和 Day 1–2，完成一个独立边界练习。 |
| 只做演示 | 没有测试、日志、README 或错误处理 | 将工程验收作为每周固定任务。 |
| 过度追新框架 | 周任务未完成却频繁切换工具 | 先完成阶段项目，再把新工具列入补充区。 |
| 时间中断 | 连续两周无法达到最小投入 | 使用 update_book.py 暂停/恢复，保留完成内容。 |
| 作品集叙事薄弱 | 只能展示界面或模型回答 | 记录问题、用户、取舍、失败案例和工程证据。 |
"""
        write(base / "ROADMAP.md", roadmap)
        write(base / "ROADMAP.mmd", mmd)
        write(base / "WEEK_INDEX.md", f"# {name}：周索引\n\n| 周次 | 执行说明 |\n|---|---|\n{weekly}\n")
        write(base / "PROJECT_PATH.md", f"# {name}：项目成长路径\n\n{project_path}\n")
        write(base / "RISKS.md", risks)
    print("Plan artifacts generated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
