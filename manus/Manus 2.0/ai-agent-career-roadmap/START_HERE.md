# 开始学习

## 第一次使用

先在本地解压目录，并使用 Python 3.12 或更高版本。执行 `python generate_files.py` 会补齐缺失文件而不默认覆盖既有笔记；执行 `python scripts/check_files.py` 检查结构；执行 `python scripts/pdf_from_markdown.py --all` 生成/刷新 PDF。

## 默认执行方案

当前方案为 **方案 C：设计师优势版**。它将设计、用户研究、信息架构与 Human-in-the-loop（人机协同）转化为工程优势，但仍要求每周完成测试、日志、数据库、部署或评测等工程证据。

## 先把控整体方向

先打开 [`INDEX.md`](INDEX.md) 查看总目录；再阅读 [`roadmap/LEARNING_OUTLINE.md`](roadmap/LEARNING_OUTLINE.md) 了解阶段逻辑，并打开 [`roadmap/LEARNING_MINDMAP.md`](roadmap/LEARNING_MINDMAP.md) 查看整体思维导图。完成这三步后，再进入当天任务。

## 今天应该做什么

打开：`weeks/week-01/days/day-01.md`。完成前不要跳到模型或多 Agent 框架。第一天的目标是建立可重复的 Python 环境、项目结构和最小测试习惯。

## 更新进度

```bash
python update_plan.py status
python update_plan.py hours --value 2.5
python update_plan.py complete --task week-01-day-01
python update_plan.py note --text "今天理解了虚拟环境的隔离作用。"
```

每次更新前，脚本会在 `.backups/` 创建备份并向 `CHANGELOG.md` 写入记录。

## 暂停、恢复和切换

```bash
python update_plan.py pause --reason "出差"
python update_plan.py resume
python update_plan.py switch-plan plan-a-foundation
```

切换仅重新安排未完成任务；原进度和个人笔记保留。
