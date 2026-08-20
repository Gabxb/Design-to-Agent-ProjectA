"""Book/tutorial layer built on top of the detailed roadmap files."""

from __future__ import annotations

from .data import PROJECTS, WEEKS, WeekSpec


class BookBuilder:
    def __init__(self, generator) -> None:  # type: ignore[no-untyped-def]
        self.g = generator

    def generate(self) -> None:
        chapters = self._chapters()
        self.g._write("book/README.md", self._readme())
        self.g._write("book/TABLE_OF_CONTENTS.md", self._toc(chapters))
        self.g._write("book/AI_AGENT_ENGINEERING_TUTORIAL.md", self._tutorial(chapters))
        for index, chapter in enumerate(chapters, start=1):
            self.g._write(f"book/chapters/{chapter['slug']}.md", chapter["content"])
        for index, project in enumerate(PROJECTS, start=1):
            project_slug = str(project["dir"]).removeprefix("project-")
            self.g._write(f"book/projects/{project_slug}.md", self._project(project, index))

    def _readme(self) -> str:
        return """# AI Agent 工程教程

这是一套按书籍顺序阅读的教程版入口。它把原本分散在 `roadmap/`、`weeks/`、`projects/`、`knowledge-base/` 和 `career/` 中的内容重新组织成“从理解到交付”的学习路径。

## 推荐阅读顺序

1. [教程目录](TABLE_OF_CONTENTS.md)
2. [完整教程正文](AI_AGENT_ENGINEERING_TUTORIAL.md)
3. 按章节打开 `chapters/`，完成章节末尾的练习。
4. 进入 `projects/` 完成对应作品集项目。
5. 回到 `weeks/` 执行每天的详细任务。

## 书籍和原始课程的关系

- `book/` 是适合连续阅读和建立整体理解的教程层。
- `weeks/` 是适合每日执行、记录和验收的课程层。
- `projects/` 是适合做作品集和模拟真实交付的项目层。
- `knowledge-base/` 是遇到概念时查阅的参考层。
- `progress/` 是学习者自己的状态层，生成器不会覆盖其中的笔记和完成记录。

## 每章学习闭环

阅读章节导入 → 完成最小练习 → 打开对应周计划 → 完成项目里程碑 → 写复盘 → 更新进度。
"""

    def _chapters(self) -> list[dict[str, str]]:
        specs = (
            ("01-foundation", "第一篇：基础工程", WEEKS[0:4], "先把想法变成可运行、可测试、可持久化的服务。"),
            ("02-llm-applications", "第二篇：LLM 应用", WEEKS[4:8], "再让模型按照结构化契约完成可靠任务，并能调用工具。"),
            ("03-rag-knowledge", "第三篇：RAG 知识库", WEEKS[8:12], "让答案基于可检索、可引用、可评测的外部知识。"),
            ("04-agent-workflows", "第四篇：Agent 工作流", WEEKS[12:16], "把单次调用升级为有状态、有边界、可人工接管的多步骤流程。"),
            ("05-production", "第五篇：生产化", WEEKS[16:20], "用测试、评测、安全、观测和部署把 Demo 变成产品。"),
            ("06-career", "第六篇：作品集与求职", WEEKS[20:24], "把技术能力转译成招聘方能够快速验证的证据。"),
        )
        return [{"slug": slug, "title": title, "content": self._chapter(slug, title, weeks, intro)} for slug, title, weeks, intro in specs]

    def _chapter(self, slug: str, title: str, weeks: tuple[WeekSpec, ...], intro: str) -> str:
        rows = "\n".join(f"| W{week.number:02d} | {week.title} | {week.deliverable} | [周计划](../../weeks/week-{week.number:02d}/WEEK_PLAN.md) |" for week in weeks)
        project_path = self.g._project_path(weeks[0])
        lessons = "\n\n".join(self._lesson(week) for week in weeks)
        return f"""# {title}

## 本篇要解决的问题

{intro}

## 能力地图

| 周 | 主题 | 交付物 | 详细入口 |
|---|---|---|---|
{rows}

## 学习方法

本篇不要按“看完概念再集中编码”的方式学习。每个主题都要走完：概念理解 → 最小例子 → 接入项目 → 错误处理 → 测试或评测 → README 表达。

## 本篇核心观点

### 1. 从边界开始

先写清用户、输入、输出、权限和不做事项，再决定模型、框架或数据库。技术选择服务于业务流程，不是为了堆名词。

### 2. 从确定性部分开始

能用代码、SQL、Schema 或状态机明确表达的规则，不交给模型自由发挥。模型负责语言理解和候选生成，系统负责校验、权限、持久化和终止。

### 3. 从失败路径证明成熟度

每个阶段至少演示一个失败：空输入、错误类型、服务超时、检索无结果、工具拒绝、人工驳回或部署失败。真实工程能力体现在失败后系统仍然可控。

## 本篇项目连接

本篇主要推进：`{project_path}`。打开项目的 `README.md`、`TASKS.md` 和 `ACCEPTANCE_CRITERIA.md`，将章节知识转成可验收交付物。

## 本篇章节

{lessons}

## 本篇练习顺序

1. 先完成 W{weeks[0].number:02d} 的 Day 01 最小示例。
2. 每周完成 `WEEK_PLAN.md` 和 `CHECKLIST.md`。
3. 每天把代码放在对应 `exercises/day-XX/`，把个人理解写在每日文件的保护区域。
4. 本篇结束时完成 W{weeks[-1].number:02d} 的项目里程碑，并写 `REVIEW.md`。

## 本篇完成标准

- [ ] 能不看教程解释本篇的核心概念。
- [ ] 能运行对应周的最小代码模板。
- [ ] 能说明一次失败、排查过程和改进。
- [ ] 项目 README、测试、验收和学习日志已更新。
- [ ] 能回答本篇周计划中的面试问题。

## 延伸阅读

- [24 周路线图](../../roadmap/24_WEEK_ROADMAP.md)
- [完整目录](../../roadmap/ROADMAP_INDEX.md)
- [本篇对应项目](../../{project_path})
"""

    def _lesson(self, week: WeekSpec) -> str:
        return f"""### 第 {week.number} 章：{week.title}

**这一章解决什么：** {week.focus}。

**为什么岗位需要：** {week.job_value}

#### 必须掌握

{self.g._bullets(week.must)}

#### 需要理解

{self.g._bullets(week.understand)}

#### 章节实践

完成“{week.deliverable}”。先运行 [Day 01 最小示例](../../weeks/week-{week.number:02d}/days/day-01.md)，再按 [本周计划](../../weeks/week-{week.number:02d}/WEEK_PLAN.md) 接入项目，最后使用 [验收清单](../../weeks/week-{week.number:02d}/CHECKLIST.md) 检查。

#### 常见风险

{week.risk}

#### 面试自检

{self.g._numbered(week.interview)}
"""

    def _toc(self, chapters: list[dict[str, str]]) -> str:
        chapter_lines = "\n".join(f"{index}. [{chapter['title']}](chapters/{chapter['slug']}.md)" for index, chapter in enumerate(chapters, start=1))
        project_lines = "\n".join(f"- [P{index}：{project['name']}](projects/{str(project['dir']).removeprefix('project-')}.md)" for index, project in enumerate(PROJECTS, start=1))
        return f"""# 教程目录

## 阅读路径

**全局地图 → 工程基础 → LLM → RAG → Agent 工作流 → 生产化 → 项目实战 → 求职交付**

## 前言

- [如何使用这本教程](README.md)
- [学习系统总纲](../roadmap/ROADMAP_OVERVIEW.md)
- [思维导图](../roadmap/ROADMAP_MINDMAP.md)

## 第一部分：六篇主教程

{chapter_lines}

## 第二部分：四个项目实战

{project_lines}

## 第三部分：参考资料

- [本地知识库](../knowledge-base/)
- [24 周详细课程](../weeks/)
- [面试资料](../interview/)
- [求职资料](../career/)
- [进度与学习日志](../progress/)

## 附录：执行命令

```bash
python update_plan.py set-day 1 1
python update_plan.py complete W01-D01-T1
python update_plan.py add-hours 1.5
python scripts/check_files.py
```
"""

    def _tutorial(self, chapters: list[dict[str, str]]) -> str:
        chapter_text = "\n\n---\n\n".join(chapter["content"].replace("../../", "../") for chapter in chapters)
        project_text = "\n\n---\n\n".join(self._project(project, index).replace("../../", "../") for index, project in enumerate(PROJECTS, start=1))
        return f"""# AI Agent 工程教程

## 前言：这不是一门只讲模型的课程

这套教程面向有设计背景和少量代码基础、希望进入 AI Agent 工程岗位的学习者。学习目标不是记住框架 API，而是完成一条真实的产品交付链：理解需求、设计数据和接口、接入模型、检索知识、编排工具、处理失败、评测效果、保障安全、部署服务，并把这些工作讲清楚。

### 使用方式

1. 先看 [教程目录](TABLE_OF_CONTENTS.md) 和 [总纲](../roadmap/ROADMAP_OVERVIEW.md)。
2. 按章节阅读本书，每章结束后打开对应周计划。
3. 每天用 `weeks/week-XX/days/day-XX.md` 执行，代码写入对应练习目录。
4. 每 4 周完成一个阶段项目，不把“读完”当作“完成”。
5. 通过 `update_plan.py` 记录完成任务、时间、问题和个人笔记。

### 贯穿全书的五个判断

- 这是一个真实用户问题，还是为了展示技术而造的 Demo？
- 哪些规则应该由代码控制，哪些内容适合交给模型？
- 如果模型、工具、数据库或用户输入失败，系统如何保持可控？
- 我用什么数据和指标证明系统变好了？
- 招聘方能否按 README 运行并理解我的取舍？

## 全书路线

**基础工程 → LLM 应用 → RAG 知识库 → Agent 工作流 → 生产化 → 求职交付**

{chapter_text}

## 项目实战篇

{project_text}

## 结语：从学习者到交付者

完成这套教程不代表掌握了所有 AI 技术，而代表你已经建立一套可以持续学习、构建、评测和交付的工作方法。接下来要做的是持续维护项目、跟踪官方文档、补充真实案例，并用面试和投递中的反馈反向改进作品集。
"""

    def _project(self, project: dict[str, object], index: int) -> str:
        base = f"../../projects/{project['dir']}"
        return f"""# P{index}：{project['name']}

## 这个项目训练什么

{project['problem']}

## 用户和业务流程

{self.g._numbered(project['workflow'])}

## 核心工程能力

{self.g._bullets(project['features'])}

## 必须证明的结果

{self.g._bullets(project['metrics'])}

## 风险边界

{self.g._bullets(project['risks'])}

## 实施入口

- [项目 README]({base}/README.md)
- [产品需求]({base}/REQUIREMENTS.md)
- [架构说明]({base}/ARCHITECTURE.md)
- [开发任务]({base}/TASKS.md)
- [验收标准]({base}/ACCEPTANCE_CRITERIA.md)
- [测试计划]({base}/TEST_PLAN.md)
- [安全说明]({base}/SECURITY.md)
- [评测方案]({base}/EVALUATION.md)
- [部署说明]({base}/DEPLOYMENT.md)

## 项目完成标准

不要只展示正常路径。至少演示一个输入错误、一个外部依赖失败、一个权限或安全边界，以及一个人工确认或明确的无答案结果。
"""
