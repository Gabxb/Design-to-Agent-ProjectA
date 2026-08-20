# 开始学习

## 第一次使用

先在本地解压目录，并使用 Python 3.12 或更高版本。执行 `python generate_book.py` 会生成或刷新教程源、地图、HTML、PDF 和报告；执行 `python scripts/check_files.py --require-pdfs` 检查结构、链接和 PDF。所有个人笔记保存在既有学习文件中，默认生成不会覆盖它们。

## 默认执行方案

当前方案为 **方案 C：设计师优势版**。它将设计、用户研究、信息架构与 Human-in-the-loop（人机协同）转化为工程优势，但仍要求每周完成测试、日志、数据库、部署或评测等工程证据。

## 先把控整体方向

先打开 [`BOOK.md`](BOOK.md) 或浏览器版 [`output/book/ai-agent-career-roadmap.html`](output/book/ai-agent-career-roadmap.html)；再阅读 [`overview/ONE_PAGE_OVERVIEW.md`](overview/ONE_PAGE_OVERVIEW.md)，并打开 [`overview/LEARNING_MAP.md`](overview/LEARNING_MAP.md) 与 [`overview/TECH_SKILL_MINDMAP.md`](overview/TECH_SKILL_MINDMAP.md)。完成这三步后，再进入当天任务。

## 今天应该做什么

打开：`weeks/week-01/days/day-01.md`。完成前不要跳到模型或多 Agent 框架。第一天的目标是建立可重复的 Python 环境、项目结构和最小测试习惯。

## 更新进度

```bash
python update_book.py status
python update_book.py complete-chapter --chapter 1
python update_plan.py hours --value 2.5
python update_plan.py complete --task week-01-day-01
python update_book.py note --text "今天理解了虚拟环境的隔离作用。"
```

每次更新前，脚本会在 `.backups/` 创建备份并向 `CHANGELOG.md` 写入记录。

## 暂停、恢复和切换

```bash
python update_plan.py pause --reason "出差"
python update_plan.py resume
python update_plan.py switch-plan plan-a-foundation
```

切换仅重新安排未完成任务；原进度和个人笔记保留。
