"""Generate the complete local learning-system artifact tree."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

from .book_builder import BookBuilder
from .data import DAY_MODES, DETAILED_DAY_TOPICS, KNOWLEDGE_TOPICS, PLANS, PROJECTS, WEEKS, WeekSpec


TODAY = date.today().isoformat()
REQUIRED_DAY_SECTIONS = (
    "## 今日目标", "## 岗位价值", "## 前置知识", "## 今日学习内容", "## 今日任务",
    "## 编码任务", "## 独立完成部分", "## 验收标准", "## 常见错误",
    "## 今天需要记录的内容", "## 补充学习区",
)
LEARNER_START = "<!-- USER_CONTENT_START -->"
LEARNER_END = "<!-- USER_CONTENT_END -->"


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    summary: str


class RoadmapGenerator:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.manifest_path = root / "config/file_manifest.json"
        self._old_manifest = self._load_manifest()
        self.generated: list[str] = []
        self.protected: list[str] = []

    def _load_manifest(self) -> dict[str, dict[str, object]]:
        if not self.manifest_path.exists():
            return {}
        try:
            entries = json.loads(self.manifest_path.read_text(encoding="utf-8")).get("files", [])
            return {str(entry["path"]): entry for entry in entries}
        except (json.JSONDecodeError, KeyError, OSError):
            return {}

    @staticmethod
    def _sha256(content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()

    def _versioned_path(self, path: Path) -> Path:
        version = 2
        while True:
            candidate = path.with_name(f"{path.stem}.v{version}{path.suffix}")
            if not candidate.exists():
                return candidate
            version += 1

    def _write(self, relative: str, content: str, *, protect: bool = False, executable: bool = False) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        encoded = content.rstrip() + "\n"

        if protect and path.exists():
            self.protected.append(relative)
            return path

        old_entry = self._old_manifest.get(relative)
        if path.exists() and old_entry and old_entry.get("generated_hash"):
            current_hash = self._sha256(path.read_bytes())
            if current_hash != old_entry["generated_hash"]:
                path = self._versioned_path(path)
                relative = path.relative_to(self.root).as_posix()
                self.protected.append(relative)

        path.write_text(encoded, encoding="utf-8")
        if executable:
            path.chmod(path.stat().st_mode | 0o111)
        self.generated.append(relative)
        return path

    def _write_json(self, relative: str, data: object, *, protect: bool = False) -> Path:
        return self._write(relative, json.dumps(data, ensure_ascii=False, indent=2), protect=protect)

    def generate_text_files(self) -> None:
        self._create_directories()
        self._generate_root_files()
        self._generate_config()
        self._generate_plans()
        self._generate_roadmap()
        self._generate_navigation()
        self._generate_book()
        self._generate_weeks()
        self._generate_exercise_scaffolds()
        self._generate_projects()
        self._generate_knowledge_base()
        self._generate_templates()
        self._generate_progress()
        self._generate_interview_and_career()
        self._generate_scripts()
        self.refresh_manifest()

    def _create_directories(self) -> None:
        directories = [
            "config", "plans", "roadmap", "weeks", "knowledge-base", "projects", "templates",
            "progress", "interview", "career", "scripts", "book", "book/chapters", "book/projects", "backups", "tmp/pdfs",
        ]
        directories += [f"plans/{name}" for name in PLANS]
        directories += [f"knowledge-base/{name}" for name in KNOWLEDGE_TOPICS]
        for week in WEEKS:
            base = f"weeks/week-{week.number:02d}"
            directories += [base, f"{base}/resources", f"{base}/notes", f"{base}/exercises", f"{base}/days"]
        for project in PROJECTS:
            base = f"projects/{project['dir']}"
            directories += [base, f"{base}/src", f"{base}/tests", f"{base}/docs", f"{base}/data", f"{base}/reference-solution"]
        for directory in directories:
            (self.root / directory).mkdir(parents=True, exist_ok=True)
        for directory in ["resources", "notes", "exercises", "src", "tests", "docs", "data", "reference-solution"]:
            for path in self.root.rglob(directory):
                keep = path / ".gitkeep"
                if not keep.exists():
                    keep.write_text("", encoding="utf-8")

    def _generate_root_files(self) -> None:
        self._write("README.md", self._root_readme())
        self._write("START_HERE.md", self._start_here())
        self._write("CHANGELOG.md", f"""# Changelog

## {TODAY}

### Added
- 创建 AI Agent 本地学习系统完整目录。
- 新增三套学习方案、24 周课程、每日任务、知识库、项目定义与进度工具。
- 新增 Markdown 到 PDF 的统一生成与校验流程。

### Changed
- 当前执行方案设置为 `plan-c-designer-ai`。

### Fixed
- 无。

### Affected Files
- 全部初始文件。
""", protect=True)
        self._write("LICENSE", """MIT License

Copyright (c) 2026 AI Agent Career Roadmap Learner

Permission is hereby granted, free of charge, to any person obtaining a copy of this learning material and associated software files, to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.
""")
        self._write("requirements.txt", """reportlab>=4.0,<5
pypdf>=5.0,<7
pdfplumber>=0.11,<1
PyYAML>=6.0,<7
""")
        self._write(".gitignore", """.env
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.DS_Store
tmp/pdfs/*.png
backups/
""")
        self._write(".env.example", """# Copy to .env and fill in only the providers you use.
LLM_API_KEY=replace_with_your_key
LLM_BASE_URL=https://api.example.com/v1
LLM_MODEL=model-name
DATABASE_URL=postgresql://app:app@localhost:5432/agent_roadmap
LOG_LEVEL=INFO
""")

    def _root_readme(self) -> str:
        return """# AI Agent Career Roadmap

这是一套可完全保存在本地、以项目驱动为核心的 AI Agent 开发学习系统。默认面向有设计背景、具备少量代码基础的学习者，当前执行方案为 **方案 C：设计师优势版**。

## 你会得到什么

- 三套可切换的学习方案：24 周稳健版、16 周求职冲刺版、20 周设计师优势版。
- 一条完整的 24 周能力课程，包含 24 份周计划和 168 份每日任务。
- 四个作品集项目定义：Tool Calling API、RAG 知识库、复杂 Agent 工作流、非设计领域综合项目。
- 一套书籍式教程：`book/AI_AGENT_ENGINEERING_TUTORIAL.md`，适合按章节连续阅读。
- 本地知识库、面试答案框架、求职清单、学习日志与进度管理工具。
- 从 Markdown 单一源文件自动生成的中文 PDF。

## 快速开始

1. 打开 [START_HERE.md](START_HERE.md)。
2. 如果想连续阅读，打开 [教程版](book/AI_AGENT_ENGINEERING_TUTORIAL.md)。
3. 用 [总纲](roadmap/ROADMAP_OVERVIEW.md) 和 [思维导图](roadmap/ROADMAP_MINDMAP.md) 建立全局方向。
4. 阅读 [方案对比](plans/PLAN_COMPARISON.md)，确认当前方案。
5. 开始 [Week 01 Day 01](weeks/week-01/days/day-01.md)。
6. 完成后更新进度：

```bash
python update_plan.py complete W01-D01-T1
python update_plan.py add-hours 1.5
python update_plan.py set-day 1 2
```

## 重新生成与检查

```bash
python generate_files.py
python generate_files.py --pdf-only
python scripts/check_files.py
```

脚本默认保留 `progress/` 中的学习记录、个人笔记和问题。修改进度前会在 `backups/` 创建备份。框架或 API 会变化，涉及具体服务时请按知识库中的检索关键词核对最新官方文档。

## 方案切换与暂停

```bash
python update_plan.py switch-plan plan-a-foundation
python update_plan.py pause --reason "工作繁忙"
python update_plan.py resume
python update_plan.py set-intensity 12
```

## 目录说明

- `plans/`：三套方案与执行映射。
- `roadmap/`：24 周路线图、能力矩阵和求职标准。
- `book/`：按书籍章节组织的教程正文、目录、项目篇和教程 PDF。
- `weeks/`：每周计划、每日任务、验收和复盘。
- `knowledge-base/`：技术主题的本地说明与示例。
- `projects/`：作品集项目需求、架构、测试、安全和部署定义。
- `progress/`：你的进度、日志、问题与已完成记录。
- `templates/`：可复制使用的学习与项目模板。

## Reference Solution 规则

`reference-solution/` 目录默认保持为空。每日任务会指出必须独立完成的部分；只有明确要求“生成参考实现”时才应写入完整答案。
"""

    def _start_here(self) -> str:
        return """# 从这里开始

当前执行方案：**方案 C：设计师优势版**  
建议投入：每周 15-20 小时  
第一阶段目标：用 4 周完成一个可测试、可持久化、可说明的 FastAPI 项目。

## 今天只做这四件事

1. 先看 [总纲与导航](roadmap/ROADMAP_OVERVIEW.md)，用 3 分钟建立全局方向。
2. 选择阅读方式：连续阅读打开 [书籍版教程](book/AI_AGENT_ENGINEERING_TUTORIAL.md)；立即动手打开 [Week 01 总计划](weeks/week-01/WEEK_PLAN.md)。
3. 打开 [思维导图](roadmap/ROADMAP_MINDMAP.md)，理解阶段、项目和求职结果如何连接。
4. 正式执行 [Day 01：安装 Python 3.12 与建立虚拟环境](weeks/week-01/days/day-01.md)。

## 第一天完成的标志

- 能在终端看到 Python 3.12 版本。
- 已创建并激活 `.venv`。
- 能运行当天的小程序。
- 已在 `progress/DAILY_LOG.md` 写下学习时间和一个问题或收获。

如果你喜欢像读书一样学习，从 [教程目录](book/TABLE_OF_CONTENTS.md) 开始；如果你喜欢边做边学，直接进入每天任务。不要先阅读全部知识库，遇到概念时再查；需要找文件时使用 [完整目录](roadmap/ROADMAP_INDEX.md)。
"""

    def _generate_config(self) -> None:
        self._write("config/learner_profile.yaml", """profile_version: 1
role: designer
coding_level: basic
target_role: AI Agent Developer
language: zh-CN
weekly_hours_default: 15
timezone: Asia/Singapore
learning_style:
  - project-driven
  - engineering-first
strengths:
  - user-research
  - interaction-design
  - information-architecture
development_stack:
  python: "3.12"
  backend: FastAPI
  database: PostgreSQL
  frontend: React or Next.js
  tools:
    - Git
    - Docker
""")
        self._write("config/current_plan.yaml", """plan: plan-c-designer-ai
plan_week: 1
source_curriculum_week: 1
status: active
selected_at: 2026-08-20
migration_note: "默认选择最能发挥设计背景优势的方案 C。"
""")
        self._write("config/learning_settings.yaml", """daily_days: 7
weekly_hours: 15
review_day: 7
preserve_user_content: true
backup_before_update: true
generate_pdf: true
pdf_language: zh-CN
code_language: en
text_encoding: UTF-8
date_format: YYYY-MM-DD
""")

    def _generate_plans(self) -> None:
        rows = []
        for plan in PLANS.values():
            rows.append(f"| {plan['name']} | {plan['weeks']} 周 | {plan['hours']} | {plan['depth']} | {plan['projects']} | {plan['jobs']} |")
        comparison = f"""# 三套 AI Agent 学习方案对比

## 快速对比

| 方案 | 周期 | 每周投入 | 技术深度 | 项目数量 | 就业方向 |
|---|---:|---:|---|---|---|
{os.linesep.join(rows)}

## 方案 A：稳健基础版

{self._plan_detail(PLANS['plan-a-foundation'])}

## 方案 B：求职冲刺版

{self._plan_detail(PLANS['plan-b-job-ready'])}

## 方案 C：设计师优势版

{self._plan_detail(PLANS['plan-c-designer-ai'])}

## 选择建议

- 每周可稳定投入 10-15 小时、希望补齐工程基础：选 A。
- 有明确求职期限、能投入 20-25 小时并接受高压：选 B。
- 希望把设计研究、产品判断和 Human-in-the-loop 变成差异化能力：选 C。

**当前默认选择 C。** 原因不是降低工程要求，而是用你已有的设计能力建立更清晰的作品集定位，同时通过数据库、测试、安全和部署验收防止偏科。
"""
        self._write("plans/PLAN_COMPARISON.md", comparison)
        for slug, plan in PLANS.items():
            mapping_lines = []
            for index, source_weeks in enumerate(plan["mapping"], start=1):
                titles = "；".join(WEEKS[n - 1].title for n in source_weeks)
                mapping_lines.append(f"| {index:02d} | {', '.join(f'W{n:02d}' for n in source_weeks)} | {titles} |")
            plan_doc = f"""# {plan['name']}

{self._plan_detail(plan)}

## 执行原则

- 根目录 `weeks/` 始终保留完整 24 周能力课程。
- 本方案通过下表把完整课程映射到 {plan['weeks']} 个执行周。
- 已完成任务使用稳定任务 ID 保存；切换方案时不会删除完成记录。
- 每个方案周开始前，根据映射打开对应源课程周，合并安排到自己的日历。

## 周映射

| 方案周 | 源课程周 | 主题 |
|---:|---|---|
{os.linesep.join(mapping_lines)}

## 使用方法

在 `progress/progress.json` 中记录当前方案周和源课程周；使用 `python update_plan.py switch-plan {slug}` 切换。切换时会生成迁移说明并备份原进度。
"""
            self._write(f"plans/{slug}/PLAN.md", plan_doc)
            self._write(f"plans/{slug}/SCHEDULE.md", plan_doc.replace("# ", "# 执行日程：", 1))
            self._write_json(f"plans/{slug}/week-mapping.json", {"plan": slug, "weeks": plan["weeks"], "mapping": plan["mapping"]})

    @staticmethod
    def _plan_detail(plan: dict[str, object]) -> str:
        return f"""- **适合人群：** {plan['audience']}
- **学习周期：** {plan['weeks']} 周
- **每周投入：** {plan['hours']}
- **学习节奏：** {plan['pace']}
- **技术深度：** {plan['depth']}
- **项目数量：** {plan['projects']}
- **就业方向：** {plan['jobs']}
- **优势：** {plan['strength']}
- **风险：** {plan['risk']}
- **选择建议：** {plan['advice']}"""

    def _generate_roadmap(self) -> None:
        phases = (
            ("第 1-4 周：编程与本地开发基础", WEEKS[0:4], "设计需求结构化助手 API"),
            ("第 5-8 周：LLM 应用开发", WEEKS[4:8], "UX Research Copilot"),
            ("第 9-12 周：RAG 知识库", WEEKS[8:12], "设计规范知识库 Agent"),
            ("第 13-16 周：Agent 工作流", WEEKS[12:16], "智能设计评审 Agent"),
            ("第 17-20 周：生产化", WEEKS[16:20], "可部署的 Agent Web 产品"),
            ("第 21-24 周：求职冲刺", WEEKS[20:24], "作品集、简历、Demo 与面试资料"),
        )
        phase_text = []
        for name, weeks, output in phases:
            week_rows = "\n".join(f"| {w.number:02d} | {w.title} | {w.deliverable} |" for w in weeks)
            phase_text.append(f"""## {name}

阶段产出：**{output}**

| 周 | 主题 | 当周产出 |
|---:|---|---|
{week_rows}
""")
        self._write("roadmap/24_WEEK_ROADMAP.md", "# 24 周 AI Agent 开发工程师路线图\n\n" + "\n".join(phase_text) + """
## 完成标准

24 周结束时，不以“看完课程”为完成，而以以下证据为准：项目可运行、有测试、有架构说明、有安全与评测设计、有可观看 Demo，并能解释关键技术取舍。
""")
        self._write("roadmap/SKILL_MATRIX.md", self._skill_matrix())
        self._write("roadmap/JOB_READY_CHECKLIST.md", """# AI Agent 工程师求职就绪检查清单

## 工程基础

- [ ] 能独立创建 Python 3.12 项目、虚拟环境和依赖文件。
- [ ] 能设计 FastAPI 接口、数据库表、错误格式和测试。
- [ ] 能使用 Git 分支、提交、Pull Request 和基本 CI。
- [ ] 能使用 Docker 启动 API 与 PostgreSQL。

## LLM、RAG 与 Agent

- [ ] 能解释 Token、上下文、Structured Output 和 Tool Calling。
- [ ] 能构建带引用、权限过滤和评测的 RAG 链路。
- [ ] 能选择 Workflow 或 Agent，并设计状态、终止、重试和人工确认。
- [ ] 能说明 MCP 的价值、安全边界和适用场景。

## 生产能力

- [ ] 有 Golden Dataset 和回归评测结果。
- [ ] 有日志、Tracing、成本、缓存和限流设计。
- [ ] 有权限、数据隔离、Prompt Injection 和 Secret 管理说明。
- [ ] 项目可以按 README 从零启动并通过测试。

## 求职材料

- [ ] 至少三个完整作品集项目，其中一个不是设计领域聊天机器人。
- [ ] 每个项目有问题、架构、数据流、失败路径、指标和取舍。
- [ ] 有 3-5 分钟 Demo 脚本和可访问演示。
- [ ] 简历使用结果和指标描述贡献。
- [ ] 能用 2 分钟、5 分钟和 15 分钟三个长度介绍核心项目。
""")

    def _generate_navigation(self) -> None:
        source_dir = Path(__file__).resolve().parent / "navigation"
        for filename in ("ROADMAP_OVERVIEW.md", "ROADMAP_INDEX.md", "ROADMAP_MINDMAP.md", "ROADMAP_MINDMAP.svg"):
            source = source_dir / filename
            if not source.exists():
                raise FileNotFoundError(f"缺少导航模板：{source}")
            self._write(f"roadmap/{filename}", source.read_text(encoding="utf-8"))

    def _generate_book(self) -> None:
        BookBuilder(self).generate()

    @staticmethod
    def _skill_matrix() -> str:
        rows = []
        for week in WEEKS:
            stage = (week.number - 1) // 4 + 1
            rows.append(f"| {week.number:02d} | {week.title} | 阶段 {stage} | {week.deliverable} |")
        return """# 能力矩阵

| 周 | 能力主题 | 阶段 | 可验证证据 |
|---:|---|---|---|
""" + "\n".join(rows) + """

## 熟练度定义

- **了解：** 能解释概念和适用边界。
- **会用：** 能在有文档支持时完成任务。
- **独立：** 能自行设计、实现、测试和排查。
- **可面试：** 能用项目证据解释取舍、失败和改进。
"""

    def _generate_weeks(self) -> None:
        for week in WEEKS:
            base = f"weeks/week-{week.number:02d}"
            self._write(f"{base}/README.md", f"# Week {week.number:02d}: {week.title}\n\n本周主计划见 [WEEK_PLAN.md](WEEK_PLAN.md)，每日任务在 `days/`。\n")
            self._write(f"{base}/WEEK_PLAN.md", self._week_plan(week))
            self._write(f"{base}/CHECKLIST.md", self._week_checklist(week))
            self._write(f"{base}/REVIEW.md", self._week_review(week), protect=True)
            for day in range(1, 8):
                self._write(f"{base}/days/day-{day:02d}.md", self._day_plan(week, day))

    def _generate_exercise_scaffolds(self) -> None:
        for week in WEEKS:
            for day in range(1, 8):
                base = f"weeks/week-{week.number:02d}/exercises/day-{day:02d}"
                topic = self._day_topic(week, day)
                task_id = f"W{week.number:02d}-D{day:02d}"
                self._write(f"{base}/README.md", f"""# {task_id} Coding Scaffold

主题：{topic}

## 文件

- `starter.py`：可直接运行的输入校验与任务上下文模板。
- `test_starter.py`：不依赖第三方库的基础测试入口。

## 运行

```bash
python starter.py
python test_starter.py
```

先让两个命令成功，再根据当天 `days/day-{day:02d}.md` 的编码任务扩展函数。核心业务函数、错误案例和项目接入部分由学习者独立完成。
""")
                self._write(f"{base}/starter.py", f'''"""Runnable scaffold for {task_id}: {topic}."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path


TASK_ID = "{task_id}"
TOPIC = "{topic}"


@dataclass(frozen=True)
class TaskContext:
    task_id: str
    topic: str
    output_path: str


def build_task_context(topic: str, output_path: str) -> TaskContext:
    cleaned_topic = " ".join(topic.strip().split())
    if not cleaned_topic:
        raise ValueError("topic must not be empty")
    path = Path(output_path)
    if path.is_absolute():
        raise ValueError("output_path must be project-relative")
    return TaskContext(task_id=TASK_ID, topic=cleaned_topic, output_path=path.as_posix())


def main() -> None:
    context = build_task_context(TOPIC, "output/result.json")
    print(json.dumps(asdict(context), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
''')
                self._write(f"{base}/test_starter.py", '''"""Dependency-free checks for the daily scaffold."""

from starter import TOPIC, build_task_context


def test_valid_context() -> None:
    context = build_task_context(TOPIC, "output/result.json")
    assert context.topic
    assert context.output_path == "output/result.json"


def test_empty_topic_is_rejected() -> None:
    try:
        build_task_context("   ", "output/result.json")
    except ValueError as exc:
        assert "topic" in str(exc)
    else:
        raise AssertionError("empty topic should be rejected")


if __name__ == "__main__":
    test_valid_context()
    test_empty_topic_is_rejected()
    print("starter checks passed")
''')

    def _week_plan(self, week: WeekSpec) -> str:
        overview = []
        for day, (mode, purpose) in enumerate(DAY_MODES, start=1):
            topic = self._day_topic(week, day)
            overview.append(f"| Day {day} | {topic} | {mode} | {self._day_hours(week, day)} 小时 |")
        return f"""# Week {week.number:02d}：{week.title}

## 1. 本周目标

- 建立对“{week.focus}”的工作级理解。
- 完成：{week.deliverable}。
- 能结合项目解释本周至少两个技术取舍。

## 2. 对应岗位能力

{week.job_value}

## 3. 每日任务总览

| 日期 | 主题 | 方式 | 预计时间 |
|---|---|---|---:|
{os.linesep.join(overview)}

## 4. 时间分配

- 概念与示例：20%
- 编码与项目：55%
- 测试、文档与排查：15%
- 复习与自由补充：10%

## 5. 必须掌握

{self._bullets(week.must)}

## 6. 需要理解

{self._bullets(week.understand)}

## 7. 暂时了解

{self._bullets(week.explore)}

## 8. 本周编码任务

- 在 `weeks/week-{week.number:02d}/exercises/` 完成最小练习。
- 在对应项目目录中完成一个可运行里程碑。
- 为关键成功路径和一个错误路径增加测试或验证脚本。

## 9. 本周项目里程碑

{week.project}：{week.deliverable}。

## 10. 工程要求

- Python 代码使用类型提示；配置不写死本地路径。
- API Key 只从环境变量读取；日志不记录完整密钥或敏感资料。
- 写清运行命令、输入输出、失败表现和验收方法。

## 11. 验收标准

- [ ] 交付物可以按 README 运行。
- [ ] 正常输入和至少一个错误输入被验证。
- [ ] 本周代码、测试、文档和进度记录均已更新。
- [ ] 能口头回答本周面试问题并引用项目例子。

## 12. 常见风险

{week.risk}

## 13. 补做任务

- 如果本周未完成，先保留核心闭环：输入 -> 处理 -> 输出 -> 错误处理 -> 运行说明。
- 将非核心优化移到 Day 7 或下一周 `REVIEW.md` 的待办区。

## 14. 提前完成后的进阶任务

- 增加一个失败场景、性能指标或安全约束。
- 对比教学版与生产版差异，并写出一条架构决策记录。

## 15. 本周面试问题

{self._numbered(week.interview)}

## 16. 周末复盘方式

展示交付物 5 分钟；说明目标、实现、失败、修复和下一步；再填写 `REVIEW.md`。

## 17. 下周准备事项

确认当前代码已提交、环境可重建、未完成任务已记录，并预览下一周的产出定义。
"""

    def _day_plan(self, week: WeekSpec, day: int) -> str:
        mode, purpose = DAY_MODES[day - 1]
        topic = self._day_topic(week, day)
        task_id = f"W{week.number:02d}-D{day:02d}"
        detailed = week.number <= 4
        explanation = self._detailed_explanation(week, day) if detailed else self._framework_explanation(week, day)
        coding = self._coding_task(week, day, detailed)
        hours = self._day_hours(week, day)
        return f"""# Day {day}：{topic}

## 今日目标

- {purpose}。
- 产出一个可以打开、运行或检查的文件，而不只停留在阅读。
- 用自己的话记录它与“{week.deliverable}”的关系。

## 岗位价值

{week.job_value}

## 前置知识

- 会打开终端、编辑文本文件并根据错误信息定位文件与行号。
- 已完成本周前一天任务；如果没有，先完成最小补做闭环。
- 不要求提前掌握本周所有概念。

## 今日学习内容

{explanation}

## 今日任务

### 任务 1：学习与最小验证

- **任务 ID：** `{task_id}-T1`
- **预计时间：** {max(0.5, hours * 0.35):.1f} 小时
- **难度：** {'入门' if week.number <= 4 else '中等'}
- **输入：** 当天主题、知识库文档和已有项目代码
- **输出：** 一份可运行最小示例或结构化学习笔记
- **文件路径：** `weeks/week-{week.number:02d}/exercises/day-{day:02d}/`

### 任务 2：接入项目

- **任务 ID：** `{task_id}-T2`
- **预计时间：** {max(0.75, hours * 0.45):.1f} 小时
- **难度：** {'入门到中等' if week.number <= 4 else '中等到进阶'}
- **输入：** 最小示例、项目需求和前一天输出
- **输出：** 与本周交付物直接相关的功能、测试或文档改动
- **文件路径：** `{self._project_path(week)}`

### 任务 3：验证与记录

- **任务 ID：** `{task_id}-T3`
- **预计时间：** {max(0.25, hours * 0.20):.1f} 小时
- **难度：** 入门
- **输入：** 今天的运行结果和错误记录
- **输出：** 验收勾选、学习日志和一个 Git 提交
- **文件路径：** `progress/DAILY_LOG.md`

## 编码任务

{coding}

## 独立完成部分

- 由你独立编写核心处理函数或工作流节点，不直接照抄完整答案。
- 至少独立设计一个错误输入及预期结果。
- `reference-solution/` 默认为空；只有明确要求后才生成参考实现。

## 验收标准

- [ ] 功能可以运行
- [ ] 输入输出符合要求
- [ ] 错误输入被正确处理
- [ ] 密钥没有写进代码
- [ ] README 已更新
- [ ] 学习记录已完成

## 常见错误

- **环境不一致：** 确认终端使用的是项目虚拟环境和正确 Python 版本。
- **只验证成功路径：** 主动构造空输入、错误类型或外部服务失败。
- **修改太大无法定位：** 缩小到最小示例，再逐步接回项目。
- **框架接口变化：** 用知识库中的官方文档名称或检索关键词核对当前版本。

## 今天需要记录的内容

- 实际学习时间、完成的任务 ID、一个最重要的理解、一个问题和下一步。
- 把命令、错误关键信息和最终解决方法写入 `progress/DAILY_LOG.md`，不要只写“已解决”。

## 补充学习区

{LEARNER_START}
### 我的理解

### 我遇到的问题

### 我的解决方法

### 需要以后复习的内容

### 自定义补充
{LEARNER_END}
"""

    def _day_topic(self, week: WeekSpec, day: int) -> str:
        if week.number in DETAILED_DAY_TOPICS:
            return DETAILED_DAY_TOPICS[week.number][day - 1]
        mode = DAY_MODES[day - 1][0]
        if day == 7:
            return f"{week.title}复习、复盘与补做"
        return f"{week.title}：{mode}"

    @staticmethod
    def _day_hours(week: WeekSpec, day: int) -> float:
        base = (1.5, 2.0, 2.25, 2.0, 2.5, 2.5, 1.5)[day - 1]
        if week.number >= 21:
            base += 0.25
        return base

    def _detailed_explanation(self, week: WeekSpec, day: int) -> str:
        explanations: dict[tuple[int, int], str] = {
            (1, 1): "虚拟环境是项目专属的 Python 工具箱，用来隔离依赖版本。先确认 `python --version` 为 3.12，再用 `python -m venv .venv` 创建环境。激活后安装的包只属于当前项目。把它理解为设计文件内嵌字体与组件版本：缺少隔离时，另一个项目的升级可能让当前项目突然失效。",
            (1, 2): "类型提示不是为了让 Python 变成强类型语言，而是提前说明数据契约。`list[str]` 表示字符串列表，`dict[str, int]` 表示键为字符串、值为整数的字典。对 Agent 工程而言，清晰类型能减少工具参数、状态字段和 API 数据之间的误解。",
            (1, 3): "函数把输入、处理和输出封装为可测试单元。异常用于表示无法正常完成的情况，例如需求文本为空。今天要区分“返回空结果”和“抛出错误”：前者是合法业务结果，后者是调用方需要处理的失败。",
            (1, 4): "类适合表达同时包含状态和行为的对象，但不要为了面向对象而创建类。先把需求看作信息对象，再决定是否用 `dataclass` 或普通类。职责要单一：解析文本的类不应同时负责写数据库和发送网络请求。",
            (1, 5): "模块是一个 Python 文件，包是包含多个模块的目录。配置应从环境变量或配置对象进入，不要散落在函数中。今天把前几天代码整理为 `src/` 包，让导入关系和入口清楚。",
            (1, 6): "独立挑战要求你只根据输入输出和验收标准完成需求清洗器。先写三个示例，再实现代码。遇到错误时保留最小失败输入，阅读 Traceback（错误追踪）最底部的异常类型和信息。",
            (1, 7): "复盘不是重新看一遍，而是从空白开始解释：环境如何建立、数据如何流动、错误如何处理、代码如何拆分。把最容易忘记的命令和概念写入知识卡片。",
            (2, 1): "Git 记录的是有意义的变更历史。一次提交应表达一个清楚意图，例如 `feat: add brief parser`。分支用于隔离尚未完成的工作。今天要建立仓库、查看差异、提交，并亲自还原一次未提交的小改动。",
            (2, 2): "HTTP（Hypertext Transfer Protocol，超文本传输协议）定义客户端和服务端如何交换请求与响应。JSON（JavaScript Object Notation）是常见数据格式。状态码不是装饰：200 表示成功，201 表示创建，400 表示请求无效，404 表示资源不存在，500 表示服务内部错误。",
            (2, 3): "REST API 把业务对象映射为资源路径，例如 `/requirements/{id}`。接口契约要说明方法、路径、输入模式、输出模式和错误。先设计契约，再写代码，可以减少前后端和工具调用之间的反复。",
            (2, 4): "FastAPI 会根据类型提示和 Pydantic 数据模型自动校验请求并生成接口文档。今天先实现 `/health` 和一个 `POST /requirements`，观察合法与非法请求的差异。",
            (2, 5): "CRUD 代表 Create、Read、Update、Delete（创建、读取、更新、删除）。先用内存列表完成路由，重点是资源 ID、状态码和响应结构，不急着接数据库。",
            (2, 6): "测试用于把预期行为固定下来。为创建成功、空标题失败和资源不存在分别写用例。不要只断言状态码，还要检查响应字段和错误格式。",
            (2, 7): "README 是陌生协作者进入项目的入口。用全新终端按 README 重跑一次，确保命令、路径和端口真实有效。",
            (3, 1): "关系数据库把稳定业务对象放入表中，用主键唯一标识记录，用外键表达关系。先从用户故事提取实体和字段，避免为了未来可能性建立过多表。",
            (3, 2): "PostgreSQL 是生产项目常用的开源关系数据库。连接字符串包含协议、用户名、密码、主机、端口和数据库名，应放在环境变量中。今天只验证连接和一条查询。",
            (3, 3): "SQL（Structured Query Language，结构化查询语言）用于读写关系数据。每次写入都要明确必填字段和默认值；更新与删除必须有条件，避免影响整张表。",
            (3, 4): "索引像内容目录，能加快特定查询但增加写入和存储成本。事务让一组操作要么全部成功，要么全部失败。今天用一个唯一约束和一个事务例子理解二者。",
            (3, 5): "API 层不应直接堆满 SQL。将数据库访问放入单独模块或 Repository（仓储）层，让路由处理 HTTP、服务层处理业务规则、数据层处理持久化。",
            (3, 6): "迁移是数据库结构的版本历史。今天模拟增加字段，并验证旧数据仍可读取。测试时使用独立数据库或回滚事务，避免污染开发数据。",
            (3, 7): "从空数据库开始按说明启动 API，创建、查询、更新和删除一条记录。把失败命令和修复步骤写入复盘。",
            (4, 1): "阶段项目先冻结范围。把“什么都能分析”缩小为明确用户、输入、输出和不做事项。每个用户故事都要能映射到接口和验收标准。",
            (4, 2): "Pydantic Schema 是数据契约。分别定义创建输入、更新输入和读取输出，避免直接暴露数据库模型。对枚举、长度和可选字段写明确约束。",
            (4, 3): "服务层负责业务规则，例如标题标准化、风险等级计算和重复需求判断。路由只负责把请求转换为服务调用，再转换为响应。",
            (4, 4): "结构化日志应包含时间、级别、事件、请求 ID 和关键结果，不应包含密钥。统一异常格式应让调用方知道错误代码、可读信息和是否可重试。",
            (4, 5): "今天完成从 HTTP 请求到数据库再到响应的完整链路。先跑手动示例，再跑自动测试，最后检查数据库记录。",
            (4, 6): "独立修复至少一个真实问题，并增加回归测试。优先处理数据校验、重复提交或不存在资源这类业务错误。",
            (4, 7): "用陌生用户视角完成验收：只看 README 启动服务，运行测试，调用接口，查看日志，再用 5 分钟讲清架构与下一阶段计划。",
        }
        return explanations[(week.number, day)]

    @staticmethod
    def _framework_explanation(week: WeekSpec, day: int) -> str:
        mode, purpose = DAY_MODES[day - 1]
        must = "、".join(week.must)
        return f"""今天处于“{mode}”节奏，核心是围绕 **{week.focus}** 完成可验证产出。先从本周必须掌握的 {must} 中选取与项目里程碑最相关的一项，运行最小示例，再接入项目。首次遇到英文缩写时，在学习日志中写出英文全称、中文含义和一个项目例子。

本文件提供完整任务结构和摘要，不替代最新框架文档。实现前使用本周知识库文档中的官方文档名称或检索关键词核对当前 API。{purpose}，并把结果与“{week.deliverable}”直接连接。"""

    def _coding_task(self, week: WeekSpec, day: int, detailed: bool) -> str:
        target = f"weeks/week-{week.number:02d}/exercises/day-{day:02d}/"
        project = self._project_path(week)
        focus = week.must[min(day - 1, len(week.must) - 1)]
        extra = "先写一个失败测试，再实现最少代码让它通过。" if day in (4, 6) else "先写清输入输出示例，再开始实现。"
        detail_note = "今天给出了更具体的实现边界，但核心函数仍需独立完成。" if detailed else "这是后续周任务框架；开始当天应结合当前项目状态补充具体函数名。"
        return f"""- **创建文件：** 在 `{target}` 创建 `README.md`、一个 Python 练习文件和必要测试；项目改动放在 `{project}`。
- **实现内容：** 围绕“{focus}”实现一个最小函数、API、检索步骤或工作流节点。
- **输入输出：** 输入使用 2 个正常示例和 1 个错误示例；输出必须可被代码检查，不只靠肉眼判断。
- **运行方式：** 在练习 README 中写出实际命令，例如 `python -m ...` 或 `pytest ...`。
- **成功判断：** 命令退出码为 0，正常案例符合预期，错误案例返回明确错误，且没有真实密钥。
- **执行提示：** {extra} {detail_note}"""

    @staticmethod
    def _project_path(week: WeekSpec) -> str:
        if week.number <= 8:
            return "projects/project-01-tool-calling/"
        if week.number <= 12:
            return "projects/project-02-rag-knowledge-base/"
        if week.number <= 16:
            return "projects/project-03-agent-workflow/"
        return "projects/project-04-capstone/"

    def _week_checklist(self, week: WeekSpec) -> str:
        return f"""# Week {week.number:02d} Checklist

- [ ] 已阅读 `WEEK_PLAN.md` 并确认本周交付物。
- [ ] 已完成 Day 1-7 的核心任务或记录补做计划。
- [ ] 已完成：{week.deliverable}。
- [ ] 已验证正常输入、错误输入和一次环境重建。
- [ ] 项目 README、测试和变更记录已更新。
- [ ] 没有真实 API Key、个人隐私或敏感业务资料进入仓库。
- [ ] 已填写 `REVIEW.md` 和 `progress/WEEKLY_STATUS.md`。
- [ ] 能回答：{week.interview[0]}
"""

    def _week_review(self, week: WeekSpec) -> str:
        return f"""# Week {week.number:02d} Review

{LEARNER_START}
## 本周完成

## 可展示证据

## 实际学习时间

## 最难的问题与解决过程

## 我现在能独立完成什么

## 仍然不稳定的能力

## 未完成任务与补做日期

## 下周调整

## 本周面试回答草稿

问题：{week.interview[0]}
{LEARNER_END}
"""

    def _generate_projects(self) -> None:
        for project in PROJECTS:
            base = f"projects/{project['dir']}"
            self._write(f"{base}/README.md", self._project_readme(project))
            self._write(f"{base}/REQUIREMENTS.md", self._project_requirements(project))
            self._write(f"{base}/ARCHITECTURE.md", self._project_architecture(project))
            self._write(f"{base}/TASKS.md", self._project_tasks(project))
            self._write(f"{base}/ACCEPTANCE_CRITERIA.md", self._project_acceptance(project))
            self._write(f"{base}/TEST_PLAN.md", self._project_test_plan(project))
            self._write(f"{base}/SECURITY.md", self._project_security(project))
            self._write(f"{base}/EVALUATION.md", self._project_evaluation(project))
            self._write(f"{base}/DEPLOYMENT.md", self._project_deployment(project))
            self._write(f"{base}/CHANGELOG.md", f"# Changelog\n\n## {TODAY}\n\n- 初始化项目定义与工程骨架。\n", protect=True)
            self._write(f"{base}/.env.example", """LLM_API_KEY=replace_with_your_key
LLM_MODEL=model-name
DATABASE_URL=postgresql://app:app@db:5432/app
LOG_LEVEL=INFO
""")
            package = str(project["dir"]).replace("-", "_")
            self._write(f"{base}/pyproject.toml", f"""[project]
name = "{project['dir']}"
version = "0.1.0"
description = "Portfolio project specification; implementation is learner-owned."
requires-python = ">=3.12"
dependencies = ["fastapi", "uvicorn", "pydantic", "sqlalchemy", "psycopg[binary]"]

[project.optional-dependencies]
dev = ["pytest", "httpx", "ruff"]

[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
""")
            self._write(f"{base}/docker-compose.yml", """services:
  api:
    build: .
    env_file: .env
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
      POSTGRES_DB: app
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 5s
      timeout: 3s
      retries: 10
    volumes:
      - postgres_data:/var/lib/postgresql/data
volumes:
  postgres_data:
""")
            self._write(f"{base}/reference-solution/README.md", "# Reference Solution\n\n默认不提供完整实现。只有学习者明确要求“生成参考实现”时才向此目录写入代码。\n", protect=True)
            self._write(f"{base}/src/__init__.py", f'''"""Starter package for {project['name']}."""\n''')
            self._write(f"{base}/src/contracts.py", f'''"""Initial API contracts; extend them as project requirements are implemented."""

from __future__ import annotations

from pydantic import BaseModel, Field


class TaskRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=20_000)


class TaskResponse(BaseModel):
    task_id: str
    project: str = "{project['name']}"
    status: str
''')
            self._write(f"{base}/src/main.py", f'''"""Minimal runnable API surface for {project['name']}."""

from __future__ import annotations

from fastapi import FastAPI


app = FastAPI(title="{project['name']}", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {{"status": "ok", "project": "{project['dir']}"}}
''')
            self._write(f"{base}/tests/test_health.py", '''"""Starter health-check test."""

from fastapi.testclient import TestClient

from src.main import app


def test_health() -> None:
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
''')

    def _project_readme(self, project: dict[str, object]) -> str:
        return f"""# {project['name']}

领域：{project['domain']}

## 项目目标

{project['problem']}

## 目标用户

{self._bullets(project['users'].split('、'))}

## 核心能力

{self._bullets(project['features'])}

## 开发方式

本目录当前提供完整需求、架构、任务、测试、安全、评测和部署定义，不提供完整参考实现。按照 `TASKS.md` 逐步在 `src/` 和 `tests/` 中实现。

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install -e ".[dev]"
pytest
```

具体框架版本和模型 API 可能变化，实施时核对最新官方文档。
"""

    def _project_requirements(self, project: dict[str, object]) -> str:
        stories = "\n".join(f"- 作为{user}，我希望系统能{project['workflow'][i % len(project['workflow'])]}，以便减少重复工作并保留可核查证据。" for i, user in enumerate(project["users"].split("、")))
        return f"""# {project['name']} 产品需求

## 1. 问题定义

{project['problem']}

## 2. 用户与场景

{project['users']}在真实业务流程中需要可追踪、可复核、可人工接管的自动化支持。

## 3. 用户故事

{stories}

## 4. 核心流程

{self._numbered(project['workflow'])}

## 5. 功能需求

{self._bullets(project['features'])}

## 6. 非功能需求

- P95 API 延迟、错误率和单次成本可记录。
- 所有外部调用有超时、重试上限和明确失败结果。
- 敏感操作需权限检查；高风险结论需人工确认。
- 项目可以通过 Docker Compose 启动，并有健康检查。

## 7. 不做事项

- 不把模型输出直接当作最终业务决定。
- 不在首版实现通用聊天机器人或无限制自主执行。
- 不使用真实个人、客户或供应商隐私数据作为演示数据。

## 8. 成功指标

{self._bullets(project['metrics'])}

## 9. 风险

{self._bullets(project['risks'])}
"""

    def _project_architecture(self, project: dict[str, object]) -> str:
        flow = " -> ".join(project["workflow"])
        return f"""# {project['name']} 架构说明

## 1. 架构目标

让业务状态、模型推理、工具执行、人工确认和审计记录彼此分离，任何失败都能定位和恢复。

## 2. 逻辑组件

| 组件 | 职责 |
|---|---|
| Web/API | 输入校验、认证、请求 ID、响应格式 |
| Application Service | 业务规则、状态转移、事务边界 |
| Agent/Workflow | 规划或节点编排、终止条件、人工中断 |
| Retrieval | 文档解析、检索、过滤、重排和引用 |
| Tools | 外部 API、数据库查询和确定性计算 |
| Persistence | 用户、任务、状态、工具调用、评测和审计 |
| Observability | 日志、Tracing、指标和成本 |

## 3. 数据流

`{flow}`

每一步都写入任务 ID、状态、开始时间、结束时间和结果摘要。外部工具原始返回在进入模型前做字段过滤。

## 4. 状态模型

- `created`：请求已接收。
- `processing`：解析、检索或工具调用中。
- `awaiting_approval`：等待人工确认。
- `completed`：产生最终可交付结果。
- `failed`：达到重试上限，保留可恢复上下文。

## 5. 关键取舍

- 确定性业务规则放在代码，不交给模型自由判断。
- Tool Calling 只允许白名单工具，每次调用前后均验证。
- RAG 与生成分别评测，避免只看最终答案。
- 首版使用单 Agent/工作流；只有独立角色确实降低复杂度时才引入多 Agent。

## 6. 教学版与生产版

教学版可使用同步调用和本地数据库；生产版需要队列或后台任务、连接池、权限、限流、重试策略、审计、监控和可回滚部署。
"""

    @staticmethod
    def _project_tasks(project: dict[str, object]) -> str:
        return f"""# {project['name']} 开发任务

## Milestone 1：最小业务闭环

- [ ] 定义请求、响应、错误与状态 Schema。
- [ ] 实现健康检查和一个核心业务接口。
- [ ] 保存任务与状态，写一个成功测试和一个失败测试。

## Milestone 2：AI 能力

- [ ] 定义 Prompt、Structured Output 和工具模式。
- [ ] 加入超时、重试上限、降级与调用日志。
- [ ] 为模型异常输出增加修复或失败策略。

## Milestone 3：证据与控制

- [ ] 接入 RAG 或业务工具，并保留来源。
- [ ] 加入人工确认和权限检查。
- [ ] 建立至少 20 条 Golden Dataset。

## Milestone 4：交付

- [ ] 完成 Docker、测试、评测、安全和部署文档。
- [ ] 准备演示数据、架构图和 5 分钟 Demo。
- [ ] 用全新环境按 README 验证一次。
"""

    @staticmethod
    def _project_acceptance(project: dict[str, object]) -> str:
        return f"""# {project['name']} 验收标准

- [ ] 核心业务流程端到端可运行。
- [ ] 输入、输出和错误均符合 Schema。
- [ ] 所有工具调用有参数校验、超时和审计记录。
- [ ] 高风险操作不会绕过人工确认。
- [ ] RAG 回答包含可核查引用，权限过滤在检索前生效。
- [ ] 测试覆盖成功、非法输入、工具失败和权限失败。
- [ ] 评测报告包含基线、指标、失败案例和改进结论。
- [ ] 日志不包含 API Key 或完整敏感文档。
- [ ] Docker Compose 可启动服务，健康检查通过。
- [ ] README、架构、安全、部署和变更记录完整。
"""

    @staticmethod
    def _project_test_plan(project: dict[str, object]) -> str:
        return f"""# {project['name']} 测试计划

## 单元测试

- Schema 校验、业务规则、状态转移、权限判断和确定性工具。

## 集成测试

- API + 数据库；检索 + 生成；Agent 节点 + Checkpoint；外部工具失败。

## 端到端场景

- 一个正常流程、一个缺失资料流程、一个权限拒绝流程、一个人工驳回流程。

## 非功能检查

- 并发、超时、重试、重复请求、日志脱敏、成本上限和恢复能力。

测试中使用合成数据和 Mock，不调用真实付费或高权限服务。
"""

    @staticmethod
    def _project_security(project: dict[str, object]) -> str:
        risks = "\n".join(f"- **威胁：** {risk}。**控制：** 代码级校验、最小权限、审计和人工复核。" for risk in project["risks"])
        return f"""# {project['name']} 安全说明

## 资产

用户身份、业务资料、Prompt、模型输出、工具凭据、审计记录和评测数据。

## 信任边界

浏览器/API、应用服务、模型供应商、检索库、外部工具和管理员后台之间均视为独立边界。

## 主要威胁与控制

{risks}

## 必须实施

- Secret 只来自环境或 Secret Manager。
- 工具白名单、参数 Schema、用户权限和资源范围同时校验。
- 文档中的指令视为不可信数据，不能覆盖系统规则。
- 日志默认脱敏；高风险操作记录操作者、原因和结果。
"""

    @staticmethod
    def _project_evaluation(project: dict[str, object]) -> str:
        return f"""# {project['name']} 评测方案

## 数据集

至少 20 个代表性案例：正常、边界、缺失信息、冲突信息、恶意输入和权限限制。

## 指标

{RoadmapGenerator._bullets(project['metrics'])}

## 分层评测

1. 输入解析与 Schema 有效率。
2. 检索召回、过滤和引用正确性。
3. 工具选择与参数准确率。
4. 工作流状态、终止和人工确认正确率。
5. 最终结果的任务完成度、事实性和可操作性。

## 回归规则

每次修改 Prompt、模型、切块、检索或工作流后运行同一数据集；关键安全案例必须 100% 通过，否则禁止发布。
"""

    @staticmethod
    def _project_deployment(project: dict[str, object]) -> str:
        return f"""# {project['name']} 部署说明

## 环境

- Python 3.12
- PostgreSQL 16
- Docker 与 Docker Compose

## 部署前

- 创建生产环境变量，禁止提交 `.env`。
- 运行测试、数据库迁移和 Golden Dataset 回归。
- 确认健康检查、日志、Tracing、限流和成本告警。

## 发布

1. 构建带版本标签的镜像。
2. 在预发布环境运行迁移和冒烟测试。
3. 发布应用，监控错误率、延迟和工具失败。
4. 指标异常时回滚镜像；数据库变更必须有兼容策略。

## 验证

- `/health` 返回正常。
- 完成一个正常场景和一个权限拒绝场景。
- 日志能用请求 ID 串联完整链路。
"""

    def _generate_knowledge_base(self) -> None:
        for slug, topic in KNOWLEDGE_TOPICS.items():
            self._write(f"knowledge-base/{slug}/README.md", self._knowledge_doc(topic))

    @staticmethod
    def _knowledge_doc(topic: dict[str, str]) -> str:
        return f"""# {topic['title']}

## 1. 这是什么

{topic['what']}

## 2. 为什么 Agent 开发需要它

它参与 Agent 的输入、状态、工具、数据、评测或部署链路，是把模型能力变成可维护产品的基础。

## 3. 设计师可以如何理解

{topic['analogy']}

## 4. 最小代码示例

```python
{topic['code']}
```

## 5. 工作中的使用方式

{topic['work']}

## 6. 教学简化方案

先用一个输入、一个处理步骤、一个输出和一个错误案例跑通，不追求通用抽象。

## 7. 生产环境方案

{topic['prod']}

## 8. 常见错误

- 只验证顺利案例。
- 把配置、密钥或本地路径写死。
- 没有记录版本、输入、输出与失败原因。

## 9. 排查方法

缩小为最小复现；核对输入类型和环境；读取最底层错误；检查日志中的请求 ID；再核对最新官方文档。

## 10. 面试问题

1. 这个技术解决什么问题，什么时候不该用？
2. 教学版到生产版需要增加哪些能力？
3. 请结合你的项目说明一次失败和改进。

## 11. 与其他技术的关系

{topic['related']}

## 12. 官方文档名称或检索关键词

`{topic['keywords']}`

框架与 API 可能变化，实施时以最新官方文档为准，不依赖二手教程中的旧接口。

## 13. 最后核对日期

{TODAY}

## 14. 我的补充笔记

{LEARNER_START}

{LEARNER_END}
"""

    def _generate_templates(self) -> None:
        templates = {
            "DAILY_NOTE_TEMPLATE.md": "# YYYY-MM-DD Daily Note\n\n## 今日目标\n\n## 完成任务 ID\n\n## 实际时间\n\n## 关键理解\n\n## 错误与解决\n\n## 明日第一步\n",
            "WEEKLY_REVIEW_TEMPLATE.md": "# Week XX Review\n\n## 交付物\n\n## 完成证据\n\n## 时间\n\n## 难点\n\n## 未完成\n\n## 下周调整\n",
            "PROJECT_README_TEMPLATE.md": "# Project Name\n\n## Problem\n\n## Users\n\n## Architecture\n\n## Setup\n\n## Tests\n\n## Evaluation\n\n## Security\n\n## Demo\n",
            "PROJECT_REQUIREMENT_TEMPLATE.md": "# Requirements\n\n## Problem\n\n## User Stories\n\n## Workflow\n\n## Functional Requirements\n\n## Non-functional Requirements\n\n## Out of Scope\n\n## Acceptance Criteria\n",
            "CODE_REVIEW_TEMPLATE.md": "# Code Review\n\n## Behavior\n\n## Bugs and Risks\n\n## Tests\n\n## Security\n\n## Maintainability\n\n## Decision\n",
            "LEARNING_LOG_TEMPLATE.md": "# Learning Log\n\n- Date:\n- Task IDs:\n- Hours:\n- Output:\n- Problem:\n- Solution:\n- Next step:\n",
            "INTERVIEW_ANSWER_TEMPLATE.md": "# Interview Answer\n\n## Question\n\n## Short Answer\n\n## Project Example\n\n## Trade-off\n\n## Failure and Improvement\n\n## Follow-up Questions\n",
        }
        for name, content in templates.items():
            self._write(f"templates/{name}", content)

    def _generate_progress(self) -> None:
        self._write_json("progress/progress.json", {
            "current_plan": "plan-c-designer-ai", "current_week": 1, "current_day": 1,
            "completed_tasks": [], "learning_hours": 0.0, "skills": {}, "problems": [],
            "custom_notes": [], "status": "active", "paused_at": None, "resume_plan": [],
            "plan_history": [], "last_updated": TODAY,
        }, protect=True)
        progress_files = {
            "DAILY_LOG.md": "# Daily Learning Log\n\n在每天结束时追加日期、任务 ID、实际时间、关键理解、问题、解决过程和下一步。\n",
            "WEEKLY_STATUS.md": "# Weekly Status\n\n每周追加：计划、实际、交付物、未完成任务、下周调整。\n",
            "SKILL_PROGRESS.md": "# Skill Progress\n\n| Skill | Level | Evidence | Last Updated |\n|---|---|---|---|\n",
            "PROBLEMS.md": "# Problems\n\n记录可复现步骤、错误信息、尝试、解决方法和需要复习的知识。\n",
            "COMPLETED_TASKS.md": "# Completed Tasks\n\n由 `update_plan.py complete TASK_ID` 追加完成记录。\n",
        }
        for name, content in progress_files.items():
            self._write(f"progress/{name}", content, protect=True)

    def _generate_interview_and_career(self) -> None:
        categories = {
            "python.md": ("Python 与工程基础", ("类型提示的价值是什么？", "如何组织一个可维护 Python 包？", "如何处理和记录异常？")),
            "api.md": ("API", ("如何设计资源和状态码？", "如何设计幂等接口？", "如何排查慢 API？")),
            "database.md": ("数据库", ("索引的收益与成本是什么？", "事务解决什么问题？", "如何设计 Agent 状态表？")),
            "llm.md": ("LLM", ("Token 与上下文窗口是什么？", "Structured Output 如何提高可靠性？", "怎样控制成本？")),
            "rag.md": ("RAG", ("Chunk 如何选择？", "为什么需要 Hybrid Search 和 Reranking？", "如何分别评测检索和答案？")),
            "agent.md": ("Agent", ("Agent 与 Workflow 如何选择？", "如何设计终止条件？", "何时使用 Human-in-the-loop？")),
            "system-design.md": ("系统设计", ("设计一个企业知识 Agent。", "如何实现租户隔离？", "如何应对模型或工具故障？")),
            "project-questions.md": ("项目问答", ("项目解决了什么真实问题？", "最难的技术取舍是什么？", "评测结果如何推动改进？")),
            "behavioral.md": ("行为面试", ("为什么从设计转向 Agent 工程？", "讲一次独立排查问题的经历。", "如何处理需求不清和时间不足？")),
        }
        for filename, (title, questions) in categories.items():
            blocks = "\n\n".join(f"## {i}. {q}\n\n### 30 秒回答\n\n### 项目证据\n\n### 取舍与失败\n" for i, q in enumerate(questions, start=1))
            self._write(f"interview/{filename}", f"# {title}面试题\n\n{blocks}")
        career = {
            "RESUME_GUIDE.md": "# 技术简历指南\n\n每个项目用“问题 - 行动 - 技术 - 结果”表达。突出可运行证据、评测、安全、成本与业务结果，不写只学习过某框架。\n",
            "PORTFOLIO_GUIDE.md": "# 作品集指南\n\n每个案例说明用户、约束、架构、数据流、失败路径、评测、取舍和下一步。界面截图只是证据之一，核心是工程闭环。\n",
            "GITHUB_CHECKLIST.md": "# GitHub Checklist\n\n- [ ] 主页简介和技术方向清晰\n- [ ] 置顶 3-4 个项目\n- [ ] README 命令可运行\n- [ ] 无密钥和大文件\n- [ ] 有测试、架构图、License 和发布记录\n",
            "DEMO_SCRIPT.md": "# 5 分钟 Demo 脚本\n\n1. 30 秒说明问题与用户。\n2. 60 秒演示正常任务。\n3. 60 秒演示证据、工具或状态。\n4. 45 秒演示错误或人工确认。\n5. 60 秒说明架构与安全。\n6. 45 秒说明评测结果和下一步。\n",
            "JOB_APPLICATION_CHECKLIST.md": "# 求职投递检查清单\n\n- [ ] 岗位技能与项目证据逐条对应\n- [ ] 简历为岗位定制\n- [ ] GitHub 和 Demo 可访问\n- [ ] 准备 2/5/15 分钟项目介绍\n- [ ] 记录投递日期、联系人、阶段和跟进\n- [ ] 面试后 24 小时内复盘问题\n",
        }
        for name, content in career.items():
            self._write(f"career/{name}", content)

    def _generate_scripts(self) -> None:
        self._write("scripts/README.md", """# 自动化脚本

运行环境：Python 3.12。首次使用先在项目根目录执行 `python -m pip install -r requirements.txt`。

- `setup.sh` / `setup.ps1`：创建虚拟环境、安装依赖、生成文件与 PDF。
- `generate_pdfs.sh` / `generate_pdfs.ps1`：只从 Markdown 重新生成 PDF。
- `check_files.py`：检查目录、数量、JSON/YAML、Python、链接、密钥模式和 PDF。
- `backup_progress.py`：单独备份 `progress/`。

macOS/Linux 使用 Shell 脚本；Windows PowerShell 使用 `.ps1` 脚本。中文 PDF 需要系统中有 Noto Sans CJK、苹方、微软雅黑、黑体或其他可嵌入中文字体；也可通过 `ROADMAP_CJK_FONT` 指定字体文件。
""")
        self._write("scripts/setup.sh", """#!/usr/bin/env sh
set -eu
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python generate_files.py
echo "完成。请打开 START_HERE.md"
""", executable=True)
        self._write("scripts/setup.ps1", """$ErrorActionPreference = "Stop"
python -m venv .venv
& .\\.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python generate_files.py
Write-Host "完成。请打开 START_HERE.md"
""")
        self._write("scripts/generate_pdfs.sh", """#!/usr/bin/env sh
set -eu
python generate_files.py --pdf-only
""", executable=True)
        self._write("scripts/generate_pdfs.ps1", """$ErrorActionPreference = "Stop"
python generate_files.py --pdf-only
""")
        self._write("scripts/check_files.py", """#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from roadmap_builder.generator import RoadmapGenerator

result = RoadmapGenerator(ROOT).validate(write_report=True)
print(result.summary)
raise SystemExit(0 if result.ok else 1)
""", executable=True)
        self._write("scripts/backup_progress.py", """#!/usr/bin/env python3
from datetime import datetime
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "progress"
target = ROOT / "backups" / datetime.now().strftime("%Y-%m-%d-%H%M%S") / "progress"
target.parent.mkdir(parents=True, exist_ok=True)
shutil.copytree(source, target)
print(target)
""", executable=True)

    @staticmethod
    def _bullets(items: Iterable[object]) -> str:
        return "\n".join(f"- {item}" for item in items)

    @staticmethod
    def _numbered(items: Iterable[object]) -> str:
        return "\n".join(f"{index}. {item}" for index, item in enumerate(items, start=1))

    def generate_pdfs(self) -> None:
        from .pdf_renderer import markdown_to_pdf

        targets: list[tuple[Path, Path]] = [
            (self.root / "book/AI_AGENT_ENGINEERING_TUTORIAL.md", self.root / "book/AI_AGENT_ENGINEERING_TUTORIAL.pdf"),
            (self.root / "plans/PLAN_COMPARISON.md", self.root / "plans/PLAN_COMPARISON.pdf"),
            (self.root / "roadmap/ROADMAP_OVERVIEW.md", self.root / "roadmap/ROADMAP_OVERVIEW.pdf"),
            (self.root / "roadmap/24_WEEK_ROADMAP.md", self.root / "roadmap/24_WEEK_ROADMAP.pdf"),
            (self.root / "roadmap/JOB_READY_CHECKLIST.md", self.root / "roadmap/JOB_READY_CHECKLIST.pdf"),
        ]
        for week in WEEKS:
            base = self.root / f"weeks/week-{week.number:02d}"
            targets.append((base / "WEEK_PLAN.md", base / "WEEK_PLAN.pdf"))
        for project in PROJECTS:
            base = self.root / "projects" / str(project["dir"])
            targets += [(base / "REQUIREMENTS.md", base / "REQUIREMENTS.pdf"), (base / "ARCHITECTURE.md", base / "ARCHITECTURE.pdf")]
        for source, output in targets:
            if not source.exists():
                raise FileNotFoundError(source)
            output.parent.mkdir(parents=True, exist_ok=True)
            markdown_to_pdf(source, output)
            self.generated.append(output.relative_to(self.root).as_posix())

    def refresh_manifest(self) -> None:
        files: list[dict[str, object]] = []
        now = datetime.now().isoformat(timespec="seconds")
        old = self._old_manifest
        for path in sorted(p for p in self.root.rglob("*") if p.is_file() and "backups" not in p.parts and "tmp" not in p.parts):
            relative = path.relative_to(self.root).as_posix()
            if relative == "config/file_manifest.json":
                continue
            digest = self._sha256(path.read_bytes())
            previous = old.get(relative, {})
            week_match = re.search(r"week-(\d{2})", relative)
            plan_match = re.search(r"plans/(plan-[^/]+)", relative)
            topic_match = re.search(r"knowledge-base/([^/]+)", relative)
            files.append({
                "path": relative, "file_type": path.suffix.lstrip(".") or "text",
                "plan": plan_match.group(1) if plan_match else None,
                "week": int(week_match.group(1)) if week_match else None,
                "topic": topic_match.group(1) if topic_match else None,
                "created_at": previous.get("created_at", now), "updated_at": now,
                "user_modified": relative in self.protected,
                "generated_hash": digest, "status": "generated",
            })
        payload = {"generated_at": now, "root": self.root.as_posix(), "files": files}
        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
        self.manifest_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def validate(self, *, write_report: bool = False) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []
        expected = ["README.md", "START_HERE.md", "config/current_plan.yaml", "plans/PLAN_COMPARISON.md", "roadmap/24_WEEK_ROADMAP.md", "progress/progress.json"]
        expected += [f"weeks/week-{w:02d}/WEEK_PLAN.md" for w in range(1, 25)]
        expected += [f"weeks/week-{w:02d}/days/day-{d:02d}.md" for w in range(1, 25) for d in range(1, 8)]
        missing = [item for item in expected if not (self.root / item).exists()]
        errors += [f"缺失文件：{item}" for item in missing]

        day_files = list((self.root / "weeks").glob("week-*/days/day-*.md")) if (self.root / "weeks").exists() else []
        if len(day_files) != 168:
            errors.append(f"每日文件数量应为 168，实际为 {len(day_files)}")
        for path in day_files:
            text = path.read_text(encoding="utf-8")
            missing_sections = [section for section in REQUIRED_DAY_SECTIONS if section not in text]
            if missing_sections:
                errors.append(f"{path.relative_to(self.root)} 缺少栏目：{', '.join(missing_sections)}")

        for json_path in self.root.rglob("*.json"):
            try:
                json.loads(json_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"JSON 无效：{json_path.relative_to(self.root)} ({exc})")

        for yaml_path in [self.root / "config/learner_profile.yaml", self.root / "config/current_plan.yaml", self.root / "config/learning_settings.yaml"]:
            if not self._basic_yaml_is_valid(yaml_path):
                errors.append(f"YAML 结构无效：{yaml_path.relative_to(self.root)}")

        for py_path in self.root.rglob("*.py"):
            try:
                compile(py_path.read_text(encoding="utf-8"), str(py_path), "exec")
            except SyntaxError as exc:
                errors.append(f"Python 语法错误：{py_path.relative_to(self.root)} ({exc})")

        exercise_starters = list((self.root / "weeks").glob("week-*/exercises/day-*/starter.py")) if (self.root / "weeks").exists() else []
        if len(exercise_starters) != 168:
            errors.append(f"每日代码模板数量应为 168，实际为 {len(exercise_starters)}")

        current_plan = self.root / "config/current_plan.yaml"
        if current_plan.exists() and "plan: plan-c-designer-ai" not in current_plan.read_text(encoding="utf-8"):
            errors.append("默认方案不是 plan-c-designer-ai")

        for slug, plan in PLANS.items():
            mapping = self.root / f"plans/{slug}/week-mapping.json"
            if mapping.exists():
                data = json.loads(mapping.read_text(encoding="utf-8"))
                if len(data.get("mapping", [])) != plan["weeks"]:
                    errors.append(f"{slug} 周映射数量不正确")

        secret_patterns = (r"sk-[A-Za-z0-9]{20,}", r"AKIA[0-9A-Z]{16}")
        for path in self.root.rglob("*"):
            if not path.is_file() or path.suffix.lower() in {".pdf", ".png", ".jpg"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if any(re.search(pattern, text) for pattern in secret_patterns):
                errors.append(f"疑似真实密钥：{path.relative_to(self.root)}")

        required_pdfs = [self.root / "book/AI_AGENT_ENGINEERING_TUTORIAL.pdf", self.root / "plans/PLAN_COMPARISON.pdf", self.root / "roadmap/ROADMAP_OVERVIEW.pdf", self.root / "roadmap/24_WEEK_ROADMAP.pdf", self.root / "roadmap/JOB_READY_CHECKLIST.pdf"]
        required_pdfs += [self.root / f"weeks/week-{w:02d}/WEEK_PLAN.pdf" for w in range(1, 25)]
        for project in PROJECTS:
            required_pdfs += [self.root / "projects" / str(project["dir"]) / "REQUIREMENTS.pdf", self.root / "projects" / str(project["dir"]) / "ARCHITECTURE.pdf"]
        for pdf in required_pdfs:
            if not pdf.exists():
                warnings.append(f"PDF 尚未生成：{pdf.relative_to(self.root)}")
                continue
            if pdf.stat().st_size < 1000:
                errors.append(f"PDF 文件异常小：{pdf.relative_to(self.root)}")
        if all(pdf.exists() for pdf in required_pdfs):
            self._validate_pdf_text(required_pdfs, errors, warnings)

        summary = f"检查完成：{len(errors)} 个错误，{len(warnings)} 个警告，{len(day_files)} 份每日任务。"
        result = ValidationResult(not errors, tuple(errors), tuple(warnings), summary)
        if write_report:
            report = self._validation_report(result, len(day_files), len(required_pdfs))
            (self.root / "GENERATION_REPORT.md").write_text(report, encoding="utf-8")
        return result

    @staticmethod
    def _validate_pdf_text(pdfs: list[Path], errors: list[str], warnings: list[str]) -> None:
        try:
            from pypdf import PdfReader
        except ImportError:
            PdfReader = None  # type: ignore[assignment,misc]
        fallback_available = __import__("shutil").which("pdftotext")
        if PdfReader is None and not fallback_available:
            return
        for pdf in pdfs:
            try:
                if PdfReader is not None:
                    reader = PdfReader(str(pdf))
                    if not reader.pages:
                        errors.append(f"PDF 无页面：{pdf}")
                        continue
                    sample = "".join((page.extract_text() or "") for page in reader.pages[:3])
                    page_texts = [(page.extract_text() or "") for page in reader.pages]
                else:
                    import subprocess
                    extracted = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
                    sample = extracted[:12000]
                    page_texts = [extracted]
                if len(sample.strip()) < 20:
                    errors.append(f"PDF 无可抽取文本或可能乱码：{pdf}")
                if "□" in sample or "�" in sample:
                    errors.append(f"PDF 检测到乱码字符：{pdf}")
                for page_number, page_text in enumerate(page_texts, start=1):
                    if len(page_text.strip()) < 3:
                        errors.append(f"PDF 疑似空白页：{pdf} 第 {page_number} 页")
            except Exception as exc:  # noqa: BLE001
                errors.append(f"PDF 无法读取：{pdf} ({exc})")

    @staticmethod
    def _basic_yaml_is_valid(path: Path) -> bool:
        if not path.exists():
            return False
        previous_indent = 0
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            if not raw_line.strip() or raw_line.lstrip().startswith("#"):
                continue
            if "\t" in raw_line:
                return False
            indent = len(raw_line) - len(raw_line.lstrip(" "))
            if indent % 2 != 0:
                return False
            stripped = raw_line.strip()
            if stripped.startswith("- "):
                if indent == 0:
                    return False
            elif ":" not in stripped:
                return False
            if indent > previous_indent + 2:
                return False
            previous_indent = indent
        return True

    def _validation_report(self, result: ValidationResult, daily_count: int, pdf_count: int) -> str:
        errors = "\n".join(f"- {item}" for item in result.errors) or "- 无"
        warnings = "\n".join(f"- {item}" for item in result.warnings) or "- 无"
        total_files = sum(1 for p in self.root.rglob("*") if p.is_file() and "tmp" not in p.parts and "backups" not in p.parts)
        return f"""# 文件生成报告

生成日期：{datetime.now().isoformat(timespec='seconds')}

## 结果

- 状态：{'通过' if result.ok else '未通过'}
- 文件总数：{total_files}
- 周目录：{len(list((self.root / 'weeks').glob('week-*'))) if (self.root / 'weeks').exists() else 0}
- 每日任务：{daily_count}
- 每日代码模板：{len(list((self.root / 'weeks').glob('week-*/exercises/day-*/starter.py'))) if (self.root / 'weeks').exists() else 0}
- 目标 PDF：{pdf_count}
- 受保护或版本化文件：{len(self.protected)}

## 错误

{errors}

## 警告

{warnings}

## 第一份应该阅读的文件

`START_HERE.md`，随后打开 `weeks/week-01/days/day-01.md`。
"""
