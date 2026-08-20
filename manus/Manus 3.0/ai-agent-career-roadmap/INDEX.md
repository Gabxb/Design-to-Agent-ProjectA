# AI Agent 学习系统总目录

> **一句话方向：**以“设计师的用户洞察与体验设计优势”为起点，逐步补齐 Python、API、数据库、LLM、RAG、Agent、评测、安全与部署能力，最终交付可演示、可解释、可求职的 AI Agent 作品集。

## 当前学习定位

| 项目 | 当前设置 |
|---|---|
| 默认方案 | **方案 C：设计师优势版** |
| 当前起点 | Week 01 / Day 01 |
| 默认投入 | 每周 15–20 小时 |
| 终点 | 3 个设计场景项目、1 个非设计综合项目、简历、Demo 与面试答案库 |
| 核心原则 | 项目驱动、工程验收、Human-in-the-loop（人机协同）、可追溯与安全优先 |

## 先看全局

| 想解决的问题 | 打开文件 | 用途 |
|---|---|---|
| 想按教程书籍连续学习？ | [教程书籍首页](book/README.md) | 按“前言—6 个分部—24 章—附录”建立连贯学习路径。 |
| 我该先做什么？ | [START_HERE.md](START_HERE.md) | 首次使用、今日起点、进度更新命令。 |
| 整个方向是什么？ | [学习大纲](roadmap/LEARNING_OUTLINE.md) | 按阶段理解能力递进、项目成果与求职闭环。 |
| 想一眼看清整体？ | [思维导图](roadmap/LEARNING_MINDMAP.md) | 使用图形化层级查看主线、阶段、项目和保障系统。 |
| 三套方案如何选择？ | [方案对比](plans/PLAN_COMPARISON.md) | 对比 A、B、C 的周期、节奏、风险与适用人群。 |
| 24 周逐周怎么推进？ | [24 周路线图](roadmap/24_WEEK_ROADMAP.md) | 从 Week 01 到 Week 24 的主题、产出和项目映射。 |
| 今天具体做什么？ | [Week 01 / Day 01](weeks/week-01/days/day-01.md) | 当前默认第一天的独立任务、代码练习和验收。 |

## 按时间导航

| 时间尺度 | 文件或目录 | 你会得到什么 |
|---|---|---|
| 今天 | `weeks/week-XX/days/day-XX.md` | 最多 3 个目标、编码任务、独立完成部分、验收和日志提示。 |
| 本周 | `weeks/week-XX/WEEK_PLAN.md` | 每日概览、时间分配、里程碑、工程要求、风险与面试问题。 |
| 每四周 | `roadmap/24_WEEK_ROADMAP.md` | 一个阶段能力闭环和可展示成果。 |
| 全周期 | `roadmap/LEARNING_OUTLINE.md` | 从工程基础到求职的完整能力地图。 |

## 按能力主线导航

| 能力主线 | 周次 | 关键问题 | 主要成果 |
|---|---:|---|---|
| 工程基础 | 1–4 | 如何把设计语言转成稳定的后端能力？ | 设计需求结构化助手 API |
| LLM 应用 | 5–8 | 如何让模型输出可约束、工具调用可控？ | UX Research Copilot |
| RAG 知识库 | 9–12 | 如何让回答有依据、可引用、可隔离？ | 设计规范知识库 Agent |
| Agent 工作流 | 13–16 | 如何让多步骤 AI 流程可恢复、可中断、可人工确认？ | 智能设计评审 Agent |
| 生产化 | 17–20 | 如何评测、保护、观测和部署一个 Agent 产品？ | 可部署 Agent Web 产品 |
| 求职冲刺 | 21–24 | 如何把工程成果讲清楚、演示出来并应对面试？ | 作品集、简历、Demo、面试库 |

## 按作品集项目导航

| 项目 | 场景 | 核心证明 | 入口 |
|---|---|---|---|
| 项目 01 | 设计需求分析 | API、Tool Calling、数据库、测试和 Docker | [project-01-tool-calling](projects/project-01-tool-calling/README.md) |
| 项目 02 | 设计规范知识管理 | 文档解析、检索、引用、权限隔离和 RAG 评测 | [project-02-rag-knowledge-base](projects/project-02-rag-knowledge-base/README.md) |
| 项目 03 | 智能设计评审 | 状态图、工具调用、人工确认、Tracing 与成本统计 | [project-03-agent-workflow](projects/project-03-agent-workflow/README.md) |
| 项目 04 | 案例分流与合规 | RAG、工作流、安全、评测、部署和非设计领域迁移能力 | [project-04-capstone](projects/project-04-capstone/README.md) |

## 按学习动作导航

| 你需要做的事 | 位置 | 规则 |
|---|---|---|
| 记录完成情况 | `progress/progress.json`、`progress/DAILY_LOG.md` | 每天记录实际耗时、完成事实、问题和下一步。 |
| 管理问题 | `progress/PROBLEMS.md` | 记录可复现问题、已尝试方案和后续排查。 |
| 复盘 | `weeks/week-XX/REVIEW.md` | 用完成事实、失败样例、工程改进和下周风险复盘。 |
| 补充知识 | `knowledge-base/` | 每个主题都有说明、最小代码、生产化差异、错误与面试问题。 |
| 准备求职 | `career/`、`interview/` | 将项目转化为简历描述、Demo 和结构化面试回答。 |
| 调整计划 | `update_plan.py` | 先备份，再暂停、恢复、切换方案或记录后续重规划。 |

## 推荐阅读顺序

```text
START_HERE
  → book / README（前言与目录）
    → 第 01 部 / 第 01 章
      → Week 01 / WEEK_PLAN
        → Week 01 / Day 01
          → progress / DAILY_LOG

需要全局回顾时：学习大纲 → 思维导图
```

当你感到“任务很多、不知道重点”时，回到本文件，然后只回答三个问题：**我现在在哪个阶段？本周需要交付什么？今天最小的可验证下一步是什么？**

## 目录结构速览

```text
ai-agent-career-roadmap/
├── INDEX.md                    # 总目录：从整体到行动的导航入口
├── START_HERE.md               # 首次启动与今天任务
├── plans/                      # 三套独立学习方案与对比
├── book/                       # 书籍式教程：前言、6 个分部、24 章和附录
├── roadmap/                    # 24 周路线图、能力矩阵、大纲、思维导图
├── weeks/                      # 24 个周学习包；每周含 7 天任务
├── knowledge-base/             # 可本地维护的技术知识库
├── projects/                   # 4 个作品集项目定义与教学骨架
├── templates/                  # 日志、复盘、项目和面试模板
├── progress/                   # 当前进度、问题、完成记录和恢复计划
├── interview/                  # 技术、项目和行为面试资料
├── career/                     # 简历、GitHub、Demo 和投递材料
├── config/                     # 学习者配置、当前方案、文件清单
└── scripts/                    # 初始化、生成 PDF、检查与备份脚本
```
