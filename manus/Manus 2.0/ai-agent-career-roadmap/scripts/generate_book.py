#!/usr/bin/env python3
"""Create a book-style tutorial reading layer for the AI Agent learning system.

The original weeks/, projects/, knowledge-base/ and progress/ folders remain the
source materials and exercises. This script adds book/ as a reading-first layer.
Existing book files are preserved by default; pass --force to rebuild them.
"""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORCE = False
written: list[str] = []
skipped: list[str] = []

PARTS = [
    {
        "number": 1,
        "title": "从设计问题到可运行服务",
        "weeks": range(1, 5),
        "promise": "建立 Python、API、数据库、测试与本地开发的工程地基。",
        "project": "设计需求结构化助手 API",
        "project_path": "project-01-tool-calling",
        "knowledge": ["python", "fastapi", "database", "git", "docker"],
        "focus": "先把设计需求转化为明确的数据模型、接口契约和验收标准，再接入任何模型能力。",
        "exit": "能独立运行一个带输入验证、错误处理、日志和测试的 FastAPI 服务。",
    },
    {
        "number": 2,
        "title": "让模型输出可靠且工具调用受控",
        "weeks": range(5, 9),
        "promise": "学习将 LLM 的灵活能力装入明确的任务、Schema、工具和安全边界。",
        "project": "UX Research Copilot",
        "project_path": "project-01-tool-calling",
        "knowledge": ["llm", "prompt-engineering", "tool-calling", "security"],
        "focus": "模型负责提出建议；应用代码负责验证、授权、执行和记录。",
        "exit": "能展示结构化输出、受控 Tool Calling、超时重试和基础注入防护。",
    },
    {
        "number": 3,
        "title": "让知识回答有证据、可引用、可评测",
        "weeks": range(9, 13),
        "promise": "构建 RAG 知识服务，处理文档、检索、引用、隔离与质量评测。",
        "project": "设计规范知识库 Agent",
        "project_path": "project-02-rag-knowledge-base",
        "knowledge": ["rag", "database", "evaluation", "security"],
        "focus": "检索结果不是答案；只有可追溯的证据、恰当引用与失败分析才能构成可靠知识服务。",
        "exit": "能在无证据时诚实拒答，并用 Golden Dataset 找到检索或生成失败的原因。",
    },
    {
        "number": 4,
        "title": "把 Agent 设计成可控的人机协同工作流",
        "weeks": range(13, 17),
        "promise": "把多步骤 AI 任务设计为有状态、有终止条件、可恢复并能人工介入的流程。",
        "project": "智能设计评审 Agent",
        "project_path": "project-03-agent-workflow",
        "knowledge": ["agent", "langgraph", "mcp", "tool-calling", "security"],
        "focus": "优先选择确定性 Workflow；只在有价值的环节引入模型驱动决策，并把高风险动作交给人工确认。",
        "exit": "能解释状态、节点、分支、检查点、工具权限和 Human-in-the-loop 的设计取舍。",
    },
    {
        "number": 5,
        "title": "从原型走向可评测、可观测、可部署的产品",
        "weeks": range(17, 21),
        "promise": "建立测试、评测、可观测性、安全、Docker、部署和运行手册能力。",
        "project": "案例分流与合规助手",
        "project_path": "project-04-capstone",
        "knowledge": ["evaluation", "security", "deployment", "docker", "agent"],
        "focus": "演示成功不代表产品可靠；你需要用评测、日志、权限、限流、部署和回滚证据证明系统可交付。",
        "exit": "能以合成数据运行端到端流程，并说明质量、安全、成本和故障处理边界。",
    },
    {
        "number": 6,
        "title": "将工程成果转化为作品集与求职证据",
        "weeks": range(21, 25),
        "promise": "把学习输出整理为招聘方能理解、验证和追问的项目材料。",
        "project": "全作品集",
        "project_path": "project-04-capstone",
        "knowledge": ["python", "rag", "agent", "evaluation", "deployment"],
        "focus": "用问题、用户、架构、取舍、失败案例和可运行 Demo 讲项目，而不是只展示界面或泛泛描述技术栈。",
        "exit": "能完成简历素材、GitHub 项目页、5 分钟 Demo、技术问答与模拟工作任务。",
    },
]

WEEKS = [
    ("Python 环境、命令行与可维护脚本", "可重复运行的 Python 命令行小工具", "虚拟环境、函数、类型提示、文件路径"),
    ("Python 数据建模、异常与测试", "含单元测试的数据转换模块", "dataclass、异常、pytest"),
    ("Git、HTTP、JSON 与 FastAPI", "带输入验证的 REST API", "Git 分支、HTTP 状态码、Pydantic"),
    ("SQL、PostgreSQL、日志与集成", "设计需求结构化助手 API 阶段版", "SQL CRUD、环境变量、日志、测试"),
    ("LLM、Token 与提示词结构", "可版本化的提示词实验记录", "上下文、角色、约束、评估样例"),
    ("结构化输出与 JSON Schema", "研究访谈洞察结构化 API", "Schema、验证、失败处理"),
    ("Tool Calling、重试与安全边界", "受控工具调用循环", "工具契约、超时、重试、审计日志"),
    ("UX Research Copilot 集成冲刺", "可演示的研究资料整理助手", "API 集成、成本记录、README"),
    ("文档解析、Chunking 与 Metadata", "可追溯的文档切分流水线", "解析、切分、元数据"),
    ("Embedding 与向量检索", "带过滤条件的基础检索服务", "嵌入、相似度、索引、过滤"),
    ("Hybrid Search、Reranking 与引用", "带引文的高质量问答链路", "关键词检索、重排、引用"),
    ("RAG 评测与数据隔离", "设计规范知识库 Agent 阶段版", "Golden Dataset、权限过滤、评测"),
    ("Workflow 与 Agent 的边界", "可审计的任务分解工作流", "状态、节点、条件分支"),
    ("LangGraph 状态图与持久化", "可恢复的状态化工作流原型", "State、Node、Edge、Checkpoint"),
    ("记忆、Human-in-the-loop 与 MCP", "带人工确认的工具工作流", "中断、批准、工具权限、MCP"),
    ("智能设计评审 Agent 集成冲刺", "可演示的设计评审工作流", "终止条件、Tracing、成本统计"),
    ("测试策略与 Agent Evaluation", "可重复运行的评测基线", "单元测试、集成测试、Golden Dataset"),
    ("Tracing、成本、缓存与安全", "具备可观测性与风险控制的服务", "结构化日志、速率限制、密钥管理"),
    ("Docker、CI/CD 与部署", "容器化、可部署的 Agent Web 产品", "Docker Compose、健康检查、CI"),
    ("产品打磨与上线演练", "可部署产品的发布候选版", "验收、回滚、运行手册"),
    ("作品集重构与架构表达", "四个项目的展示版 README 和架构图", "问题—方案—取舍—结果叙事"),
    ("简历、GitHub 与 Demo", "简历素材、主页和 Demo 脚本", "STAR、项目量化、录屏流程"),
    ("面试与系统设计", "技术问答库与系统设计白板稿", "Python、RAG、Agent、权衡"),
    ("模拟工作任务与投递复盘", "端到端模拟任务和求职跟踪系统", "需求澄清、拆分、交付、复盘"),
]


def write(relative: str, content: str) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not FORCE:
        skipped.append(relative)
        return
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    written.append(relative)


def chapter_part(week: int) -> dict[str, object]:
    return next(part for part in PARTS if week in part["weeks"])


def day_links(week: int) -> str:
    links = []
    for day in range(1, 8):
        links.append(f"[{day}](../../weeks/week-{week:02d}/days/day-{day:02d}.md)")
    return " · ".join(links)


def knowledge_links(slugs: list[str]) -> str:
    return "、".join(f"[{slug}](../../knowledge-base/{slug}/OVERVIEW.md)" for slug in slugs)


def book_readme() -> str:
    rows = []
    for part in PARTS:
        weeks = part["weeks"]
        rows.append([f"第 {part['number']} 部", part["title"], f"Week {min(weeks):02d}–{max(weeks):02d}", part["project"]])
    return f"""# 《从设计师到 AI Agent 开发工程师》

## 一本项目驱动的本地教程

这不是一套脱离练习的“阅读材料合集”。它将现有的 24 周学习系统重新编排为 **6 个分部、24 个章节、4 个项目和 1 组求职附录**。每章负责解释“为什么学、学什么、做到什么程度”，而原有的 `weeks/` 目录负责保存每天的任务、练习、验收和复盘。

> **阅读顺序：**读本书的分部导读与章节导航 → 打开对应周计划 → 完成当天任务 → 更新进度 → 回到章节做自检。

## 这本书如何使用

| 阅读层 | 位置 | 作用 |
|---|---|---|
| 总体方向 | [总目录](../INDEX.md)、[学习思维导图](../roadmap/LEARNING_MINDMAP.md) | 先判断自己位于哪一阶段，避免被细节淹没。 |
| 书籍教程层 | `book/` | 按“部—章—练习—附录”阅读，建立连贯心智模型。 |
| 每周实践层 | `weeks/` | 按 7 天节奏完成概念、编码、工程化、项目、挑战和复盘。 |
| 项目证据层 | `projects/` | 将每一阶段能力沉淀为可展示的工程项目。 |
| 进度反馈层 | `progress/` | 记录学习事实、问题、复盘和计划调整。 |

## 全书目录

| 分部 | 主题 | 对应周次 | 阶段项目 |
|---|---|---:|---|
{chr(10).join('| ' + ' | '.join(row) + ' |' for row in rows)}

## 开始阅读

1. 先读 [前言：如何把这套系统当作一本书](00_PREFACE.md)。
2. 打开 [目录](CONTENTS.md)，进入第一部分。
3. 需要快速回顾整体时，回到 [学习大纲](../roadmap/LEARNING_OUTLINE.md) 和 [思维导图](../roadmap/LEARNING_MINDMAP.md)。
4. 开始实操时，进入 [第 01 章](chapters/chapter-01.md)，随后打开对应的 [Week 01 周计划](../weeks/week-01/WEEK_PLAN.md)。

## 重要边界

本书是**导航与讲解层**，不是对现有文件的替代。请不要移动或删除 `weeks/`、`projects/`、`knowledge-base/`、`progress/` 中的内容；这些目录仍是任务、作品、笔记和进度的实际来源。
"""


def preface() -> str:
    return """# 前言：如何把这套系统当作一本书

## 你在学习的不是一串框架名称

AI Agent 开发的难点，不在于记住某个模型或框架的 API，而在于把用户需求、数据、模型、工具、状态、人工确认、评测、安全和部署连接成一个能交付的系统。你的设计背景并不是绕开的过去，而是理解用户任务、定义信息结构、安排交互边界和设计人机协同体验的基础。

## 本书的阅读节奏

每一章对应一周。先读章节中的“本章定位”和“完成标准”，再进入周计划的 7 天实践。Day 1–5 用来理解、编码、工程化和集成；Day 6 要尽量独立完成挑战；Day 7 用于复盘和补做。每章完成后，回到本章自检并更新 `progress/`。

## 三种阅读模式

| 模式 | 适用场景 | 路径 |
|---|---|---|
| 顺读 | 第一次学习 | 前言 → 分部导读 → 章节 → 周计划 → 每日任务。 |
| 任务驱动 | 今天有 1–3 小时 | 当前章节 → 当天任务 → 项目任务板 → 日志。 |
| 复习 | 准备面试或发现知识断层 | 分部导读 → 章节自检 → 知识库 → 面试附录。 |

## 完成的定义

只有在你能运行代码、解释输入输出、展示错误处理、通过测试、更新 README 并留下复盘记录时，才算完成一个章节。模型演示成功、复制了一段代码或看完视频，都不等于完成。

## 从哪里开始

现在进入 [第一部分：从设计问题到可运行服务](chapters/part-01.md)，然后开始 [第 01 章](chapters/chapter-01.md)。
"""


def contents() -> str:
    parts = []
    for part in PARTS:
        entries = []
        for week in part["weeks"]:
            title, _, _ = WEEKS[week - 1]
            entries.append(f"- [第 {week:02d} 章：{title}](chapters/chapter-{week:02d}.md)")
        parts.append(f"## [第 {part['number']} 部：{part['title']}](chapters/part-{part['number']:02d}.md)\n\n" + "\n".join(entries))
    return "# 目录\n\n" + "\n\n".join(parts) + "\n\n## 附录\n\n- [附录总览](appendices/README.md)\n- [知识库索引](appendices/knowledge-base.md)\n- [项目工作簿](appendices/projects.md)\n- [学习记录与模板](appendices/practice-system.md)\n- [求职与面试材料](appendices/career-and-interview.md)\n"


def part_content(part: dict[str, object]) -> str:
    weeks = part["weeks"]
    chapter_rows = []
    for week in weeks:
        title, output, must = WEEKS[week - 1]
        chapter_rows.append(f"| [第 {week:02d} 章](chapter-{week:02d}.md) | {title} | {output} |")
    return f"""# 第 {part['number']} 部：{part['title']}

## 本部承诺

{part['promise']}

## 为什么这一部现在出现

{part['focus']}

## 本部章节

| 章节 | 本周主题 | 本周可验证产出 |
|---|---|---|
{chr(10).join(chapter_rows)}

## 本部项目

本部的主要成果将沉淀到 **[{part['project']}](../../projects/{part['project_path']}/README.md)**。不要等到本部最后一周才打开项目目录；从第一章起就把每周产出连接到项目任务板、README 和测试中。

## 建议阅读与实践节奏

1. 先通读本部四章标题，理解能力的递进关系。
2. 每周先读章节，再读 `weeks/week-XX/WEEK_PLAN.md`。
3. 每天完成 `days/day-XX.md` 的最小闭环，并在 `progress/DAILY_LOG.md` 中写下事实。
4. Day 7 回到本部，检查你是否正向项目里程碑推进。

## 推荐配套知识库

{knowledge_links(part['knowledge'])}

## 离开本部前，你应该能做到

{part['exit']}

## 下一步

从 [第 {min(weeks):02d} 章](chapter-{min(weeks):02d}.md) 开始本部学习。
"""


def chapter_content(week: int) -> str:
    title, output, must = WEEKS[week - 1]
    part = chapter_part(week)
    first = min(part["weeks"])
    last = max(part["weeks"])
    project_path = part["project_path"]
    project = part["project"]
    if week == first:
        position = "这是本部的开章。重点是建立本部问题意识和最小实践闭环。"
    elif week == last:
        position = "这是本部的收束章。重点是将前几章能力整合为可展示里程碑，并完成复盘。"
    else:
        position = "这是本部的能力连接章。重点是把上一章的基础转成下一个关键能力，而不是孤立记忆概念。"
    previous = f"[第 {week - 1:02d} 章](chapter-{week - 1:02d}.md)" if week > 1 else "无；从前言开始"
    following = f"[第 {week + 1:02d} 章](chapter-{week + 1:02d}.md)" if week < 24 else "无；进入附录完成求职整理"
    return f"""# 第 {week:02d} 章：{title}

> 所属分部：[第 {part['number']} 部：{part['title']}](part-{part['number']:02d}.md) · 对应 Week {week:02d} · 主项目：[{project}](../../projects/{project_path}/README.md)

## 本章定位

{position} 这一章要掌握的核心是：**{must}**。

## 为什么要学这一章

本章不是为了增加一个技术关键词，而是为了让你的 Agent 系统在真实项目中更可解释、更可维护或更可交付。请在完成后用自己的项目案例解释：这个能力解决了什么用户/工程问题，失效时会造成什么风险，以及如何用代码或测试验证它。

## 本章完成标准

本章结束时应交付：**{output}**。你还应在项目目录中留下代码、测试、README 更新、任务状态或复盘中的至少一项可检验证据。

## 阅读—实践路径

| 顺序 | 打开内容 | 目的 |
|---:|---|---|
| 1 | [本周计划](../../weeks/week-{week:02d}/WEEK_PLAN.md) | 先理解目标、时间分配、里程碑与验收。 |
| 2 | {day_links(week)} | 按概念、编码、功能、工程化、项目、挑战、复盘完成实践。 |
| 3 | [本周检查清单](../../weeks/week-{week:02d}/CHECKLIST.md) | 用清单检查功能、测试、文档、安全与日志。 |
| 4 | [本周复盘](../../weeks/week-{week:02d}/REVIEW.md) | 记录事实、失败样例、改进和下周准备。 |
| 5 | [项目任务板](../../projects/{project_path}/TASKS.md) | 将本周产出连到作品集项目。 |

## 本章独立练习

不要直接寻找完整答案。完成本章之后，为核心功能补写一个你自己选择的边界样例：无效输入、外部依赖超时、权限不足、无检索证据或人工拒绝任选其一。把它放入本周 `exercises/`，并在复盘中写出你为什么选择这个失败路径。

## 本章自检

- [ ] 我可以用非术语化语言解释“{must}”在系统中的作用。
- [ ] 我完成了至少一个可运行的最小功能，而不仅是阅读。
- [ ] 我有正常路径与异常/边界路径的验证证据。
- [ ] 我没有把密钥、真实用户数据或敏感信息写入仓库。
- [ ] 我已更新本周日志、项目任务板或 README。

## 章节衔接

| 上一章 | 本章 | 下一章 |
|---|---|---|
| {previous} | Week {week:02d}：{title} | {following} |

## 本部回顾提示

你正在推进第 {part['number']} 部（Week {first:02d}–{last:02d}）。本部核心问题是：**{part['focus']}**

## 需要补充的笔记

### 我自己的解释


### 我在项目中的证据


### 我仍要复习的问题


"""


def appendices() -> dict[str, str]:
    knowledge_rows = []
    for slug in ["python", "fastapi", "database", "git", "docker", "llm", "prompt-engineering", "tool-calling", "rag", "agent", "langgraph", "mcp", "evaluation", "security", "deployment"]:
        knowledge_rows.append(f"| [{slug}](../../knowledge-base/{slug}/OVERVIEW.md) | 技术解释、最小代码、生产化差异、错误排查与面试问题 |")
    project_rows = []
    projects = [
        ("项目 01", "设计需求分析助手", "project-01-tool-calling", "API、Tool Calling、数据库、测试、Docker"),
        ("项目 02", "设计规范知识库 Agent", "project-02-rag-knowledge-base", "RAG、引用、权限隔离、评测"),
        ("项目 03", "智能设计评审 Agent", "project-03-agent-workflow", "状态工作流、人工确认、Tracing、成本"),
        ("项目 04", "案例分流与合规助手", "project-04-capstone", "非设计领域综合产品、安全、部署"),
    ]
    for number, name, path, proof in projects:
        project_rows.append(f"| {number} | [{name}](../../projects/{path}/README.md) | {proof} |")
    return {
        "README.md": """# 附录总览

附录不需要按顺序读。它们是你在实践中查阅、复盘、补充证据和准备求职时使用的工具书。

| 附录 | 何时使用 |
|---|---|
| [知识库索引](knowledge-base.md) | 遇到不理解的技术概念、错误或面试题时。 |
| [项目工作簿](projects.md) | 需要将每周产出连接到作品集项目时。 |
| [学习记录与模板](practice-system.md) | 需要记录进度、复盘、调整计划或备份时。 |
| [求职与面试材料](career-and-interview.md) | Week 21 起整理简历、Demo、GitHub 和面试答案时。 |
""",
        "knowledge-base.md": "# 附录 A：知识库索引\n\n这些文档是本书的可维护技术词典。涉及框架或模型 API 时，在实施前仍须核对最新官方文档。\n\n| 主题 | 内容 |\n|---|---|\n" + "\n".join(knowledge_rows) + "\n",
        "projects.md": "# 附录 B：项目工作簿\n\n项目不是章节结束后才开始的作业。每一章都应在对应项目中留下需求、代码、测试、文档或复盘证据。\n\n| 项目 | 入口 | 重点证明 |\n|---|---|---|\n" + "\n".join(project_rows) + "\n",
        "practice-system.md": """# 附录 C：学习记录与模板

| 目标 | 文件 |
|---|---|
| 当前状态与完成任务 | [progress.json](../../progress/progress.json)、[已完成任务](../../progress/COMPLETED_TASKS.md) |
| 每日事实和问题 | [每日学习日志](../../progress/DAILY_LOG.md)、[问题记录](../../progress/PROBLEMS.md) |
| 每周复盘 | 每周目录中的 `REVIEW.md` |
| 调整、暂停与恢复 | [update_plan.py](../../update_plan.py) |
| 写作模板 | [templates/](../../templates/) |
| 文件与结构检查 | [check_files.py](../../scripts/check_files.py) |

## 最小记录纪律

每天至少写下实际时长、完成文件、一个失败或困惑点、明天第一步。每周记录一条可以复现的错误样例和修复方式。这样你的学习日志会成为作品集和面试的真实素材，而不只是打卡记录。
""",
        "career-and-interview.md": """# 附录 D：求职与面试材料

| 目的 | 文件 |
|---|---|
| 简历项目表述 | [RESUME_GUIDE.md](../../career/RESUME_GUIDE.md) |
| 作品集结构 | [PORTFOLIO_GUIDE.md](../../career/PORTFOLIO_GUIDE.md) |
| GitHub 整理 | [GITHUB_CHECKLIST.md](../../career/GITHUB_CHECKLIST.md) |
| 5 分钟项目演示 | [DEMO_SCRIPT.md](../../career/DEMO_SCRIPT.md) |
| 投递前检查 | [JOB_APPLICATION_CHECKLIST.md](../../career/JOB_APPLICATION_CHECKLIST.md) |
| 技术与项目面试 | [interview/](../../interview/) |
| 求职就绪验证 | [JOB_READY_CHECKLIST.md](../../roadmap/JOB_READY_CHECKLIST.md) |

## 面试复习顺序

先从你实际写过的项目讲起，再用 `interview/` 补齐 Python、API、数据库、LLM、RAG、Agent 和系统设计问答。每个回答都要包含上下文、选择、取舍、证据和改进方向；不要只背定义。
""",
    }


def main() -> int:
    global FORCE
    parser = argparse.ArgumentParser(description="Generate the book-style tutorial layer.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing book files.")
    args = parser.parse_args()
    FORCE = args.force
    write("book/README.md", book_readme())
    write("book/00_PREFACE.md", preface())
    write("book/CONTENTS.md", contents())
    for part in PARTS:
        write(f"book/chapters/part-{part['number']:02d}.md", part_content(part))
    for week in range(1, 25):
        write(f"book/chapters/chapter-{week:02d}.md", chapter_content(week))
    for relative, content in appendices().items():
        write(f"book/appendices/{relative}", content)
    print(f"Written: {len(written)}; preserved: {len(skipped)}")
    for path in written:
        print(f"+ {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
