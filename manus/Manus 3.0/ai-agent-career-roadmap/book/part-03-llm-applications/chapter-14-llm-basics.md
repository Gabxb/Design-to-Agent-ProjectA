# 第 14 章：大语言模型基础

> **章节信息：**所属篇章：[第三篇：LLM 应用开发](README.md) · 对应 Week 05 · 对应项目：[project-02-rag-knowledge-base](../../projects/project-02-rag-knowledge-base/README.md) · 前置章节：本篇第一章 · 后续章节：[下一章](chapter-15-prompt-engineering.md)

## 本章导航

[返回全书目录](../../TABLE_OF_CONTENTS.md) · [返回学习地图](../../overview/LEARNING_MAP.md) · [对应周计划](../../weeks/week-05/WEEK_PLAN.md) · [本周首页](../../weeks/week-05/README.md)

## 为什么学习这一章

LLM 基于上下文预测和生成内容，不是确定性规则系统。 在 AI Agent 开发工作中并不是孤立知识点，它决定了系统能否被团队理解、测试、维护和安全地交付。本章结束时，你应能把它连接到一个具体用户任务、一个明确输入输出，以及一个可验证的工程证据。

## 设计师理解方式

把它当作需要明确任务单、输入资料和复核机制的协作伙伴。

## 学习目标

- 能用自己的话说明 大语言模型基础 在 AI Agent 系统中的责任边界。
- 能运行本章最小示例，并为一个错误/边界输入补充验证。
- 能在对应项目中指出此能力将用于何处，以及何时需要人工确认或安全控制。

## 核心概念

| 层级 | 内容 |
|---|---|
| 必须熟练 | 能解释输入、输出、失败路径和最小测试。 |
| 需要理解 | 能说明它与 API、数据库、模型、工具、状态或部署的关系。 |
| 暂时了解 | 高级性能调优、框架特定扩展或大规模生产细节。 |

## 工作原理

一个可靠实现总是先定义边界，再选择技术：先确定用户要完成的任务；再定义输入与输出契约；接着实现确定性校验与记录；最后在需要灵活判断的位置使用模型或检索。模型输出不能跳过应用层验证，更不能绕过权限、审计和人工确认。

## 最小可运行示例

**文件路径：**`book/examples/chapter-14/main.py`

```python
"""Chapter 14 teaching example: 大语言模型基础."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Evidence:
    source: str
    text: str


def build_response(question: str, evidence: list[Evidence]) -> dict[str, object]:
    if not question.strip():
        raise ValueError("question must not be empty")
    if not evidence:
        return {"answer": "没有足够证据，建议补充资料。", "citations": []}
    return {"answer": evidence[0].text, "citations": [evidence[0].source]}


if __name__ == "__main__":
    sample = [Evidence(source="synthetic-guide.md", text="大语言模型基础 的教学示例已准备。")]
    print(build_response("本章学习什么？", sample))
```

**运行命令：**

```bash
python book/examples/chapter-14/main.py
```

**预期输出：**控制台打印一个经过边界检查的教学结果。这个示例使用合成内容，不调用真实 API，不需要密钥。

**常见错误与排查：**如果出现 `ModuleNotFoundError`，先确认你位于根目录并激活虚拟环境；如果出现 `ValueError`，检查输入是否为空或超出示例允许范围。

## 教学版实现

教学版用纯 Python 和合成样例演示单一概念，省略了网络调用、真实数据库、认证与监控。这样可以先看清输入、输出和状态变化。

## 生产版考虑

生产环境还需要环境变量配置、结构化日志、异常分类、超时、重试、权限校验、数据隔离、测试、监控和回滚。框架及模型 API 可能变化，编码前应核对当前官方文档。

## 项目中的应用

本章能力将进入 **[project-02-rag-knowledge-base](../../projects/project-02-rag-knowledge-base/README.md)**。请在项目任务板中记录本章实际添加的功能、测试或文档证据，不要只完成阅读。

## 本章练习

| 练习类型 | 任务 | 完成证据 |
|---|---|---|
| 基础练习 | 运行最小示例，并解释每个输入输出。 | 一条运行记录。 |
| 修改练习 | 修改一个边界条件，并补写一个断言或手工验证。 | 修改后的代码与测试说明。 |
| 独立挑战 | 设计一个失败输入，说明系统应拒绝、重试还是交给人工。 | `exercises/` 中的实现与复盘。 |
| 项目任务 | 将本章概念连接到对应项目的一个任务。 | 更新 `TASKS.md` 或 README。 |

## 验收标准

- [ ] 最小示例可以运行。
- [ ] 能说明输入、输出与错误行为。
- [ ] 至少验证一个正常与一个异常/边界情况。
- [ ] API Key 没有写入代码或日志。
- [ ] 对应项目任务、README 或学习日志已更新。

## 常见错误

| 现象 | 优先排查方向 |
|---|---|
| 只会复述概念 | 用一个项目功能说明该概念改变了什么行为。 |
| 功能只在正常输入下成功 | 先补一个无效输入、超时或拒绝路径。 |
| 把模型输出当作最终事实 | 检查 Schema、证据、权限和人工确认边界。 |
| 文档和代码不一致 | 重新运行 README 命令并更新示例。 |

## 本章总结

1. 大语言模型基础 的核心是：LLM 基于上下文预测和生成内容，不是确定性规则系统。
2. 先定义输入、输出、错误和验收，再实现功能。
3. 教学版用于看清责任边界，生产版需要安全、观测与交付措施。
4. 项目证据比单次演示更能说明能力。

## 术语表

| 术语 | 本章中的含义 |
|---|---|
| 契约 | 对输入、输出、错误与责任边界的明确约定。 |
| 验收 | 用可观察结果确认功能符合要求。 |
| Human-in-the-loop | 在高影响节点让人类审核、批准、拒绝或修改。 |

## 我的笔记

### 我的理解


### 我遇到的问题


### 我的解决方法


### 需要复习的内容


## 章节导航

[返回全书目录](../../TABLE_OF_CONTENTS.md) · [返回学习地图](../../overview/LEARNING_MAP.md) · 本篇第一章 · [下一章](chapter-15-prompt-engineering.md) · [对应周计划](../../weeks/week-05/WEEK_PLAN.md)
