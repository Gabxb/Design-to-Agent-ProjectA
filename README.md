# 🤖 AI Agent 学习资料导航

> [!abstract] 整理说明
> 本文按照下面的路线整理：
>
> **基础认知 → 系统学习 → 项目实战 → Coding Agent → 企业级工程化**
>
> 建议不要同时学习全部资料。每个阶段选择 **1 个主线资料 + 1 个补充资料** 即可。

---

## 🧭 快速导航

| 分类 | 学习目标 |
|---|---|
| 🌱 入门与通识 | 建立 Agent、RAG、工具调用等基础认知 |
| 🧠 原理与架构 | 理解 Agent Loop、上下文、记忆和工具系统 |
| 🛠️ 项目实战 | 完成可运行的 Agent 或多 Agent 项目 |
| 💻 Coding Agent | 理解 Claude Code、Pi 等编程智能体 |
| 🏢 企业工程化 | 学习评估、安全、治理、部署和可观测性 |
| ☕ Java 方向 | 使用 Spring AI、LangChain4j 等技术落地 |

<br>

---

# 🌱 一、入门与系统通识

> [!tip] 本阶段目标
> 建立完整的 Agent 知识地图，理解常见技术名词之间的关系。

<br>

## 1. Hello-Agents

**类型：** 开源教程  
**难度：** ⭐⭐  
**推荐指数：** ⭐⭐⭐⭐⭐  
**适合作为：** 第一套系统教材

### 🔗 地址

- [在线阅读](https://hello-agents.datawhale.cc/#/)

### 📝 简介

Datawhale 推出的系统性 Agent 教程，兼顾理论和实践。

主要涉及：

- Agent 基础
- ReAct
- Dify
- LangGraph
- Memory
- RAG
- MCP
- A2A
- 多智能体
- 综合项目

> [!success] 推荐理由
> 内容比较完整，适合用来建立 Agent 开发的整体知识框架。

<br>

---

## 2. AI 智能体实战速成指南

**副标题：** 从零到企业级落地  
**类型：** 开源教程 + 项目源码  
**难度：** ⭐⭐  
**推荐指数：** ⭐⭐⭐⭐⭐  
**主要语言：** Python

### 🔗 地址

- [GitHub 仓库](https://github/didilili/ai-agents-from-zero)
- [在线阅读](https://didilili.github.io/ai-agents-from-zero/#/)

### 📝 简介

从低代码平台逐渐过渡到代码开发，主要串联：

- Dify
- Coze
- LangChain
- LangGraph
- RAG
- MCP
- DeepAgents
- 模型部署
- 企业级项目
- 面试准备

配有电商问数、深度研搜等项目。

> [!success] 推荐理由
> 很适合已经使用过 Dify，希望进一步学习 Python Agent 开发的人。

> [!warning] 链接说明
> 原记录中的 GitHub 地址缺少 `.com`，上方已经修正。

<br>

---

## 3. AI Agent Guide

**类型：** 通识教程 + 面试指南  
**难度：** ⭐⭐  
**推荐指数：** ⭐⭐⭐⭐  
**适合方向：** Java、企业应用、面试复习

### 🔗 地址

- [在线阅读](https://ai-agent-guide.xiaofuge.cn/)

### 📝 简介

内容包括：

- Agent 基础
- Function Calling
- ReAct
- Memory
- MCP
- Skills
- LangGraph
- Dify
- RAG
- Agent 安全
- Agent 评估
- 部署与运维

> [!success] 推荐理由
> 适合建立技术名词地图，也适合整理 Agent 面试知识点。

<br>

---

## 4. 深入理解 AI Agent

**英文名：** AI Agents in Depth  
**类型：** 开源技术书  
**难度：** ⭐⭐⭐  
**推荐指数：** ⭐⭐⭐⭐⭐

### 🔗 地址

- [在线阅读](https://bojieli.github.io/ai-agent-book)

### 📝 简介

围绕下面的公式展开：

> **Agent = LLM + 上下文 + 工具**

主要介绍：

- 上下文工程
- 用户记忆
- RAG 与知识库
- 工具系统
- MCP
- Coding Agent
- Agent 评估
- 多模态 Agent
- 多 Agent 协作

> [!success] 推荐理由
> 适合完成基础入门之后，用来深入理解 Agent 的设计原理。

<br>

---

## 5. AI 工程从零开始

**类型：** 完整 AI 工程课程  
**难度：** ⭐⭐⭐⭐⭐  
**推荐指数：** ⭐⭐⭐⭐  
**适合作为：** 长期学习路线

### 🔗 地址

- [在线阅读](https://liangdabiao.github.io/ai-engineering-from-scratch/site/index.html#contents)

### 📝 简介

覆盖范围非常广，包括：

- 数学基础
- 机器学习
- 深度学习
- Transformer
- LLM
- 工具与协议
- Agent Engineering
- 多智能体
- 生产基础设施

> [!warning] 学习建议
> 这套资料内容较多，不建议直接从头到尾全部学习。
>
> 可以优先阅读与 **LLM Engineering、Tools、Agent、Multi-Agent、Production** 相关的部分。

<br>

---

# 🧠 二、Agent 原理与架构进阶

> [!tip] 本阶段目标
> 不再只会调用框架，而是理解 Agent Loop、工具执行、上下文和运行时。

<br>

## 6. Learn Agent the Hard Way

**中文名：** 笨办法学 Agent  
**类型：** 开源电子书 + 可运行代码  
**主要语言：** Go  
**难度：** ⭐⭐⭐  
**推荐指数：** ⭐⭐⭐⭐⭐

### 🔗 地址

- [GitHub 仓库](https://github.com/Leihb/learn-agent-the-hard-way)
- [在线阅读](https://leihb.github.io/learn-agent-the-hard-way/)

### 📝 简介

从一个最小 Agent 循环开始，逐步实现：

- LLM API 调用
- Agent Loop
- Tool Use
- 上下文管理
- 权限控制
- Skills
- Subagent
- MCP
- 浏览器工具
- 沙箱

> [!success] 推荐理由
> 适合想摆脱框架黑盒，真正理解 Agent Harness 的开发者。

<br>

---

## 7. Agent 工程哲学

**类型：** 架构思想  
**难度：** ⭐⭐⭐⭐  
**推荐指数：** ⭐⭐⭐⭐

### 🔗 地址

- [在线阅读](https://onenightcarnival.github.io/agent-engineering-philosophy/)

### 📝 简介

这本书将 Agent 看成拥有以下要素的自主角色：

- 岗位
- 技能
- 记忆
- 权限
- 工作环境
- 工作履历

重点讨论：

- 系统提示词
- Agent Skills
- 持久化沙箱
- 长期记忆
- 授权机制
- 多 Agent 团队设计

> [!info] 阅读建议
> 这不是基础教程，更适合做过 Agent 项目之后阅读。

<br>

---

## 8. AI Agent 架构

**副标题：** 从单体到企业级多智能体  
**类型：** 多 Agent 架构  
**难度：** ⭐⭐⭐⭐  
**推荐指数：** ⭐⭐⭐⭐

### 🔗 地址

- [在线阅读](https://waylandz.com/ai-agent-book/)

### 📝 简介

聚焦单 Agent 向多 Agent 系统演进时的架构问题，可用于补充学习：

- 多智能体协作
- 任务委派
- 工作流
- 可靠执行
- 系统治理
- 企业级架构

<br>

---

## 9. Agent 设计模式之美

**类型：** 付费专栏  
**平台：** 极客时间  
**难度：** ⭐⭐⭐⭐  
**推荐指数：** ⭐⭐⭐⭐

### 🔗 地址

- [查看课程](https://time.geekbang.org/column/101162601)

### 📝 简介

主要围绕下面几个方面整理 Agent 设计模式：

- 感知
- 记忆
- 推理
- 行动
- 反思
- 协作
- 治理

> [!success] 推荐理由
> 适合已经有项目经验，希望系统学习 Agent 架构设计的人。

<br>

---

# 🛠️ 三、Agent 项目与企业级实战

> [!tip] 本阶段目标
> 独立完成一个可运行、可部署、可展示的 Agent 项目。

<br>

## 10. MCP+A2A 从 0 到 1 构建类 Manus 多 Agent 全栈应用

**平台：** 慕课网  
**类型：** 多 Agent 全栈项目  
**难度：** ⭐⭐⭐⭐  
**推荐指数：** ⭐⭐⭐⭐

### 🔗 地址

- [查看课程](https://coding.imooc.com/class/ds/955)

### 📝 主要内容

- 单 Agent
- 多 Agent
- MCP
- A2A
- 浏览器自动化
- 沙箱
- 分布式 Agent
- FastAPI
- Next.js
- Docker
- 类 Manus 项目

> [!success] 适合人群
> 已经具备 Python、API 和基础 Web 开发能力，希望完成综合项目的人。

<br>

---

## 11. AI Agent 开发项目实战

**作者：** 李文周  
**类型：** 企业级项目课程  
**主要语言：** Go  
**难度：** ⭐⭐⭐⭐  
**推荐指数：** ⭐⭐⭐⭐⭐

### 🔗 地址

- [查看课程](https://liwenzhou.com/courses/ai-agent/)

### 📝 主要内容

- 手写 LLM 接入
- Agent Loop
- MCP
- RAG
- 多智能体
- 上下文治理
- Eino
- ADK-Go
- A2A
- 企业内部 Agent 平台

> [!success] 推荐理由
> 工程化内容较完整，适合学习生产级 Agent 后端开发。

<br>

---

## 12. 黑马程序员 Agent 课程

**平台：** B站  
**类型：** 视频教程 + 项目实战  
**主要语言：** Python  
**难度：** ⭐⭐ 至 ⭐⭐⭐

### 🔍 建议搜索关键词

- `黑马程序员 Agent`
- `黑马程序员 LangChain`
- `黑马程序员 LangGraph`
- `黑马程序员 RAG`
- `黑马程序员大模型 RAG 与 Agent 实战`

### 📝 主要内容

- 大模型 API 调用
- Prompt 和消息模板
- LangChain
- LangGraph
- 向量数据库
- RAG
- ReAct
- 知识库客服
- 多 Agent 项目
- FastAPI
- Vue3

> [!warning] 说明
> 当前没有记录具体的 B 站视频地址，暂时无法准确对应唯一课程。

<br>

---

# 💻 四、Coding Agent 与 Claude Code

> [!tip] 本阶段目标
> 理解 Claude Code、Pi 等 Coding Agent 背后的运行机制。

<br>

## 13. Pi Agent Book

**类型：** Coding Agent 原理教程  
**主要语言：** TypeScript  
**难度：** ⭐⭐⭐⭐  
**推荐指数：** ⭐⭐⭐⭐⭐

### 🔗 地址

- [在线阅读](https://dg-ai-notes.pages.dev/)

### 📝 主要内容

- Pi Coding Agent
- 多模型抽象
- Agent Core
- Agent Loop
- 工具系统
- 终端 UI
- 会话管理
- 流式输出
- 扩展机制
- Agent SDK

> [!success] 推荐理由
> 适合通过一个相对精简的项目理解 Coding Agent 架构。

<br>

---

## 14. Pi Coding Agent 作者博客

**类型：** 作者设计总结  
**语言：** 英文  
**难度：** ⭐⭐⭐⭐

### 🔗 地址

- [阅读原文](https://mariozechner.at/posts/2025-11-30-pi-coding-agent/)

### 📝 主要内容

- 极简 Agent Harness
- 多模型 API
- 上下文交接
- 流式输出
- 工具调用
- 工具结果管理
- Coding Agent 设计取舍

> [!info] 阅读建议
> 建议配合 Pi Agent Book 一起阅读。

<br>

---

## 15. Learn Claude Code：交互式教程

**类型：** 在线交互教程  
**难度：** ⭐⭐  
**推荐指数：** ⭐⭐⭐⭐

### 🔗 地址

- [开始学习](https://claude.nagdy.me/learn/)

### 📝 主要内容

- Slash Commands
- CLAUDE.md
- Skills
- Hooks
- MCP
- Subagents
- Plugins

> [!success] 推荐理由
> 提供浏览器终端模拟器，适合先学习 Claude Code 的使用和配置。

<br>

---

## 16. Learn Claude Code：从零实现 Coding Agent

**类型：** 渐进式源码教程  
**难度：** ⭐⭐⭐⭐  
**推荐指数：** ⭐⭐⭐⭐⭐

### 🔗 地址

- [在线阅读](https://learn.shareai.run/zh/)

### 📝 主要内容

- Agent Loop
- Tool Use
- Permission
- Hooks
- Todo 与计划
- Subagent
- Skills
- 上下文压缩
- Memory
- Task System
- Background Tasks
- 多 Agent 协作
- 文件隔离
- MCP

> [!success] 推荐理由
> 每次增加一个机制，适合逐步理解 Coding Agent 的内部结构。

<br>

---

# 🧩 五、辅助学习工具与案例

<br>

## 17. LearnGraph

**类型：** AI 学习平台 + 开源项目  
**难度：** ⭐⭐⭐⭐  
**适合作为：** 项目参考

### 🔗 地址

- [GitHub 仓库](https://github.com/SunnyBoy-y/LearnGraph)
- [开发者文档](https://sunnyboy-y.github.io/LearnGraph/#streaming)

### 📝 项目特点

- 根据目标生成学习路线
- 使用知识图谱组织内容
- 围绕知识节点继续提问
- 记录学习证据
- Agent 工具调用
- Skills
- MCP
- 沙箱
- 长期记忆
- 流式输出

> [!success] 推荐理由
> 可以同时参考它的产品设计、Agent 架构和学习流程。

<br>

---

## 18. LearnGraph 项目介绍帖

**类型：** 社区项目介绍  
**平台：** Linux.do

### 🔗 地址

- [查看项目介绍](https://linux.do/t/topic/2666861)

### 📝 简介

作者集中介绍了 LearnGraph 的：

- 产品目标
- 学习图谱
- 智能问答
- 练习系统
- 模型支持
- 项目迭代

> [!info] 阅读建议
> 可以先阅读介绍帖了解功能，再决定是否进一步阅读源码。

<br>

---

# 🗺️ 六、推荐学习路线

## 🌱 第一阶段：建立基础认知

> 建议选择一套主线，不要全部同时学习。

1. **Hello-Agents**
2. **AI Agent Guide**
3. **AI 智能体实战速成指南**

### 阶段成果

- 能用一句话解释 Agent
- 理解 LLM、Prompt、Tool、Memory、RAG
- 能使用 Dify 搭建简单应用
- 能解释 LangChain 和 LangGraph 的区别

<br>

---

## 🧠 第二阶段：理解核心原理

1. **深入理解 AI Agent**
2. **Learn Agent the Hard Way**
3. **Learn Claude Code：从零实现 Coding Agent**

### 阶段成果

- 能手写最小 Agent Loop
- 理解工具调用循环
- 理解上下文管理
- 理解 Skills 和工具的区别
- 理解 Subagent 的基本原理

<br>

---

## 🛠️ 第三阶段：完成项目实战

选择其中一个作为主项目：

1. **慕课网类 Manus 多 Agent 项目**
2. **李文周 AI Agent 开发项目实战**
3. **黑马程序员 Agent 项目**

### 阶段成果

- 完成一个可运行的 Agent 项目
- 支持 RAG 或工具调用
- 支持流式输出
- 可以使用 Docker 部署
- 能够展示完整项目架构

<br>

---

## 🏢 第四阶段：架构与工程化

1. **Agent 工程哲学**
2. **Agent 设计模式之美**
3. **AI Agent 架构**
4. **Pi Agent Book**

### 阶段成果

- 理解 Agent Harness
- 理解多 Agent 编排
- 理解权限和沙箱
- 理解评估与可观测性
- 能分析 Agent 系统的架构取舍

<br>

---

# ☕ 七、Java 企业级 Agent 路线

> [!important] 学习建议
> 可以先用 Python 理解 Agent 核心机制，再使用 Java 完成企业级工程化落地。

## 1. Java 应用基础

- Java
- Spring Boot
- REST API
- WebSocket
- SSE
- Maven
- Gradle

## 2. Agent 开发框架

- Spring AI
- LangChain4j
- Function Calling
- Tool Calling
- Structured Output
- Agent Memory

## 3. Agent 协议

- MCP
- A2A
- Agent Skills
- JSON Schema
- OpenAPI

## 4. RAG 与知识库

- Embedding
- 向量数据库
- 文档切片
- 混合检索
- BM25
- Rerank
- GraphRAG

## 5. 数据与中间件

- PostgreSQL
- Redis
- Elasticsearch
- Kafka
- MinIO

## 6. 工程化与部署

- Docker
- Kubernetes
- CI/CD
- 日志系统
- 链路追踪
- 灰度发布

## 7. 安全与治理

- Prompt Injection 防护
- 权限控制
- 沙箱隔离
- Human-in-the-loop
- Agent Evaluation
- Agent Observability
- 审计日志
- 成本监控

<br>

---

# 📌 八、个人学习原则

> [!quote] 核心学习方法
> 先把技术名词单独拆出来，再逐个理解，最后把它们串成完整系统。

## 每个技术名词的笔记结构

```text
技术名词：
一句话解释：
它解决什么问题：
它位于系统的哪一层：
它和哪些技术有关：
最小代码示例：
常见使用场景：
容易混淆的概念：
详细解释链接：
