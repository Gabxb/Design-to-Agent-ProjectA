# AI Agent Career Roadmap

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
