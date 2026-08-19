# AI Agent Career Roadmap

**Version:** 1.0.0  
**Created:** 2024-12-19  
**Current Plan:** plan-c-designer-ai

---

## 24周学习路线图

### 第1-4周：编程与本地开发基础
- Python 3.12
- 类型提示、函数、类
- 虚拟环境、环境变量
- Git 与 GitHub
- HTTP、JSON、REST API
- FastAPI
- 基础 SQL、PostgreSQL
- 日志、异常处理、基础测试
- **产出：** "设计需求结构化助手 API"

### 第5-8周：LLM 应用开发
- LLM 基础、Token 和上下文
- Prompt 结构、Few-shot、Structured Output
- JSON Schema、Function Calling、Tool Use
- 超时、重试和降级
- 成本记录、Prompt Injection
- **产出：** "UX Research Copilot"

### 第9-12周：RAG 知识库
- 文档解析、Chunking
- Embedding、向量检索
- Metadata、Hybrid Search、Reranking
- Query Rewrite、引用溯源
- RAG 评测
- **产出：** "设计规范知识库 Agent"

### 第13-16周：Agent 工作流
- Agent 与 Workflow、ReAct
- Tool Calling、状态管理
- 条件分支、循环和终止条件
- 短期/长期记忆、Human-in-the-loop
- LangGraph、MCP
- **产出：** "智能设计评审 Agent"

### 第17-20周：生产化
- 单元测试、集成测试
- Agent Evaluation、Golden Dataset
- 日志和 Tracing、Prompt 版本管理
- 缓存、限流、权限、安全
- Docker、CI/CD、云端部署
- **产出：** "可部署的 Agent Web 产品"

### 第21-24周：求职冲刺
- 项目优化、GitHub 整理
- README、架构图、Demo 视频
- 简历、项目介绍、Python 面试
- RAG 与 Agent 面试、系统设计
- 模拟工作任务
- **产出：** 3-4 个作品集项目 + 技术简历 + GitHub 主页 + 面试资料库

---

## 每周详细计划框架

### 每周目标
### 对应岗位能力
### 每日任务总览
### 时间分配
### 必须掌握
### 需要理解
### 暂时了解
### 本周编码任务
### 本周项目里程碑
### 工程要求
### 验收标准
### 常见风险
### 补做任务
### 提前完成后的进阶任务
### 本周面试问题
### 周末复盘方式
### 下周准备事项

---

## 项目作品集

1. **设计需求分析助手** (Tool Calling + FastAPI + PostgreSQL)
2. **设计规范知识库 Agent** (RAG)
3. **智能设计评审 Agent** (复杂 Agent 工作流)
4. **设计服务平台 Agent** (综合项目，体现业务流程、RAG、Tool Calling、Agent 工作流、安全、评测、部署)

---

## 学习进度管理

- 进度文件：`progress/progress.json`
- 进度更新脚本：`update_plan.py`
- 进度备份：`scripts/backup_progress.py`

---

## 知识库

每个技术主题生成独立的本地知识文档，包括：
- 这是什么
- 为什么 Agent 开发需要它
- 设计师可以如何理解
- 最小代码示例
- 工作中的使用方式
- 教学简化方案
- 生产环境方案
- 常见错误
- 排查方法
- 面试问题
- 与其他技术的关系
- 官方文档名称或检索关键词
- 最后核对日期
- 我可以补充笔记的区域

---

## 模板

所有模板保存在 `templates/` 目录，包括：
- DAILY_NOTE_TEMPLATE.md
- WEEKLY_REVIEW_TEMPLATE.md
- PROJECT_README_TEMPLATE.md
- PROJECT_REQUIREMENT_TEMPLATE.md
- CODE_REVIEW_TEMPLATE.md
- LEARNING_LOG_TEMPLATE.md
- INTERVIEW_ANSWER_TEMPLATE.md

---

## 求职准备

- RESUME_GUIDE.md
- PORTFOLIO_GUIDE.md
- GITHUB_CHECKLIST.md
- DEMO_SCRIPT.md
- JOB_APPLICATION_CHECKLIST.md

---

## 下一阶段

请使用 `python generate_files.py` 脚本创建完整目录结构和详细文件。

**第一天任务：** 打开 `weeks/week-01/day-01.md` 并完成当日任务