# AI Agent 学习资料整理

> 按照“基础认知 → 系统学习 → 项目实战 → Coding Agent → 工程化进阶”的顺序整理。重复链接已合并，错误链接已标注。

---

## 一、入门与系统通识

### 1. Hello-Agents：从零开始构建智能体

[在线阅读](https://hello-agents.datawhale.cc/#/)

Datawhale 开源教程，兼顾理论与实践。内容涵盖 Agent 基础、ReAct、LangGraph、Dify、Memory、RAG、MCP、A2A、多智能体和综合项目，适合作为第一套系统教材。

---

### 2. AI 智能体实战速成指南：从零到企业级落地

[GitHub 仓库](https://github/didilili/ai-agents-from-zero)

[在线阅读](https://didilili.github.io/ai-agents-from-zero/#/)

以 Python 技术栈为主，串联 Dify、Coze、LangChain、LangGraph、RAG、MCP、DeepAgents、部署和面试准备，并包含电商问数、深度研搜等项目。

适合从 Dify 低代码开发过渡到代码开发。

> 注意：原链接 `https://github/didilili/ai-agents-from-zero` 缺少 `.com`，正确地址应为上面的 GitHub 链接。

---

### 3. AI Agent Guide：通识教程

[在线阅读](https://ai-agent-guide.xiaofuge.cn/)

偏向 Java 开发者的 Agent 通识与面试指南，涵盖 Agent 基础、Function Calling、Memory、MCP、Skills、LangGraph、Dify、RAG、安全、评估和部署。

适合建立 Agent 技术知识地图，也适合用于面试复习。

---

### 4. 深入理解 AI Agent：AI Agents in Depth

[在线阅读](https://bojieli.github.io/ai-agent-book)

从 `Agent = LLM + 上下文 + 工具` 出发，系统介绍上下文工程、记忆、RAG、工具、MCP、Coding Agent、评估、多模态和多 Agent 协作。

适合完成基础入门后，进一步理解 Agent 的设计原理和工程实践。

---

### 5. AI 工程从零开始

[在线阅读](https://liangdabiao.github.io/ai-engineering-from-scratch/site/index.html#contents)

覆盖数学、机器学习、Transformer、LLM、工具协议、Agent、多智能体和生产基础设施。

课程强调先理解并实现底层机制，再使用高级框架。内容规模较大，适合作为长期 AI 工程学习路线。

---

## 二、Agent 原理与架构进阶

### 6. Learn Agent the Hard Way

[GitHub 仓库](https://github.com/Leihb/learn-agent-the-hard-way)

[在线阅读](https://leihb.github.io/learn-agent-the-hard-way/)

使用 Go 从最小 Agent 循环开始，逐步实现工具调用、上下文管理、权限、Skills、Subagent、MCP、浏览器和沙箱。

适合想摆脱框架黑盒、真正理解 Agent Harness 的开发者。

---

### 7. Agent 工程哲学

[在线阅读](https://onenightcarnival.github.io/agent-engineering-philosophy/)

将 Agent 看作拥有岗位、技能、记忆和工作环境的自主角色。

重点讨论系统提示词、Skills、持久化沙箱、长期记忆、授权机制和多 Agent 团队设计。该资料偏架构思考，不属于基础入门教程。

---

### 8. AI Agent 架构：从单体到企业级多智能体

[在线阅读](https://waylandz.com/ai-agent-book/)

聚焦从单 Agent 演进到多 Agent 系统时的架构问题。

适合补充学习多智能体、任务委派、可靠执行、工作流和企业级治理等内容。

---

### 9. Agent 设计模式之美

[极客时间课程](https://time.geekbang.org/column/101162601)

围绕认知功能和执行拓扑整理 Agent 设计模式，涉及感知、记忆、推理、行动、反思、协作和治理，并结合 Coding Agent 架构进行分析。

适合已经具备一定项目经验，希望系统学习 Agent 架构设计的开发者。

---

## 三、Agent 项目与企业级实战

### 10. 慕课网：MCP+A2A 从 0 到 1 构建类 Manus 多 Agent 全栈应用

课程主页需要在慕课网搜索：

`MCP+A2A 从0到1构建类Manus多Agent全栈应用`

课程覆盖单 Agent、多 Agent、MCP、A2A、浏览器自动化、沙箱、分布式 Agent、FastAPI、Next.js 和 Docker 部署。

主线是实现一个类 Manus 的多 Agent 全栈项目，适合具备 Python 和 Web 开发基础后学习。

---

### 11. AI Agent 开发项目实战

[查看课程](https://liwenzhou.com/courses/ai-agent/)

面向 Go 开发者，从手写 LLM 接入、Agent 循环、MCP、RAG、多智能体和上下文治理开始，再进入 Eino、ADK-Go、A2A 和企业内部 Agent 平台建设。

企业工程化内容比较完整，适合希望学习生产级 Agent 后端开发的人员。

---

### 12. B站黑马程序员 Agent 课程

建议在 B 站搜索以下关键词：

- 黑马程序员 Agent
- 黑马程序员 LangChain
- 黑马程序员 LangGraph
- 黑马程序员 RAG
- 黑马程序员大模型 RAG 与 Agent 实战

相关内容主要涉及：

- 大模型 API 调用
- Prompt 与消息模板
- LangChain
- LangGraph
- 向量数据库
- RAG
- ReAct
- 知识库客服
- 多 Agent 项目
- FastAPI
- Vue3

> 当前没有提供具体的 B 站视频地址，因此暂时无法准确对应唯一课程。

---

## 四、Coding Agent 与 Claude Code 专题

### 13. Pi Agent Book

[在线阅读](https://dg-ai-notes.pages.dev/)

围绕 Pi Coding Agent 展开，介绍其编码工具、学习教材和开发 SDK 三种定位。

主要分析模型抽象、Agent Core、终端 UI、工具系统、会话管理和扩展机制，适合研究极简 Coding Agent 架构。

---

### 14. Pi Coding Agent 作者博客

[阅读原文](https://mariozechner.at/posts/2025-11-30-pi-coding-agent/)

作者总结构建极简 Coding Agent 的设计经验。

重点讨论多模型 API、上下文交接、流式输出、工具结果和最小化 Agent Harness，适合配合 Pi Agent Book 阅读。

---

### 15. Learn Claude Code：交互式教程

[开始学习](https://claude.nagdy.me/learn/)

提供浏览器内终端模拟器、配置生成器和练习，覆盖：

- Slash Commands
- CLAUDE.md
- Skills
- Hooks
- MCP
- Subagents
- Plugins

适合先学习 Claude Code 的使用方法和配置体系。

---

### 16. Learn Claude Code：从零实现 Claude Code-like Agent

[在线阅读](https://learn.shareai.run/zh/)

通过渐进式代码实现以下机制：

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

适合深入理解 Coding Agent 内部运行机制。

---

## 五、辅助学习工具与案例

### 17. LearnGraph

[GitHub 仓库](https://github.com/SunnyBoy-y/LearnGraph)

[开发者文档](https://sunnyboy-y.github.io/LearnGraph/#streaming)

AI 驱动的学习平台，可以根据学习目标生成知识路线图，并围绕知识节点组织提问、资料、练习和学习证据。

项目还涉及：

- Agent
- Tools
- Skills
- MCP
- 沙箱
- 长期记忆
- 知识图谱
- 流式输出

适合参考其产品设计和系统实现，也可以作为管理 Agent 学习路线的工具。

---

### 18. LearnGraph 项目介绍帖

[查看社区介绍](https://linux.do/t/topic/2666861)

作者对 LearnGraph 的产品目标、学习图谱、智能问答、练习、模型支持和项目迭代进行了集中介绍。

适合先了解项目功能，再决定是否进一步阅读源码。

---

## 六、推荐学习顺序

### 第一阶段：建立基础认知

1. Hello-Agents
2. AI Agent Guide
3. AI 智能体实战速成指南

### 第二阶段：理解核心原理

4. 深入理解 AI Agent
5. Learn Agent the Hard Way
6. Learn Claude Code：从零实现 Claude Code-like Agent

### 第三阶段：完成项目实战

7. 慕课网类 Manus 多 Agent 项目
8. 李文周 AI Agent 开发项目实战
9. 黑马程序员 Agent 项目课程

### 第四阶段：学习架构与工程化

10. Agent 工程哲学
11. Agent 设计模式之美
12. AI Agent 架构：从单体到企业级多智能体
13. Pi Agent Book

### 长期补充路线

14. AI 工程从零开始

---

## 七、Java 企业级 Agent 学习方向

如果主攻企业级 Java，可以重点学习以下技术：

- Java
- Spring Boot
- Spring AI
- LangChain4j
- MCP
- A2A
- Function Calling
- Agent Skills
- RAG
- Embedding
- 向量数据库
- 混合检索
- Rerank
- Redis
- PostgreSQL
- Elasticsearch
- Docker
- Kubernetes
- Agent Evaluation
- Agent Observability
- Prompt Injection 防护
- 权限控制
- 沙箱隔离
- Human-in-the-loop

建议先通过 Python 理解 Agent 的核心机制，再使用 Java 完成企业级工程化落地。
