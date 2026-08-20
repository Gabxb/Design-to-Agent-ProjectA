# 第 4 部：把 Agent 设计成可控的人机协同工作流

## 本部承诺

把多步骤 AI 任务设计为有状态、有终止条件、可恢复并能人工介入的流程。

## 为什么这一部现在出现

优先选择确定性 Workflow；只在有价值的环节引入模型驱动决策，并把高风险动作交给人工确认。

## 本部章节

| 章节 | 本周主题 | 本周可验证产出 |
|---|---|---|
| [第 13 章](chapter-13.md) | Workflow 与 Agent 的边界 | 可审计的任务分解工作流 |
| [第 14 章](chapter-14.md) | LangGraph 状态图与持久化 | 可恢复的状态化工作流原型 |
| [第 15 章](chapter-15.md) | 记忆、Human-in-the-loop 与 MCP | 带人工确认的工具工作流 |
| [第 16 章](chapter-16.md) | 智能设计评审 Agent 集成冲刺 | 可演示的设计评审工作流 |

## 本部项目

本部的主要成果将沉淀到 **[智能设计评审 Agent](../../projects/project-03-agent-workflow/README.md)**。不要等到本部最后一周才打开项目目录；从第一章起就把每周产出连接到项目任务板、README 和测试中。

## 建议阅读与实践节奏

1. 先通读本部四章标题，理解能力的递进关系。
2. 每周先读章节，再读 `weeks/week-XX/WEEK_PLAN.md`。
3. 每天完成 `days/day-XX.md` 的最小闭环，并在 `progress/DAILY_LOG.md` 中写下事实。
4. Day 7 回到本部，检查你是否正向项目里程碑推进。

## 推荐配套知识库

[agent](../../knowledge-base/agent/OVERVIEW.md)、[langgraph](../../knowledge-base/langgraph/OVERVIEW.md)、[mcp](../../knowledge-base/mcp/OVERVIEW.md)、[tool-calling](../../knowledge-base/tool-calling/OVERVIEW.md)、[security](../../knowledge-base/security/OVERVIEW.md)

## 离开本部前，你应该能做到

能解释状态、节点、分支、检查点、工具权限和 Human-in-the-loop 的设计取舍。

## 下一步

从 [第 13 章](chapter-13.md) 开始本部学习。
