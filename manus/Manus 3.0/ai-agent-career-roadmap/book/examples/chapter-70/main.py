"""Chapter 70 teaching example: 投递、复盘和持续学习."""
from __future__ import annotations


def explain(topic: str) -> str:
    if not topic.strip():
        raise ValueError("topic must not be empty")
    return f"{topic}：先定义输入、输出、约束和验收证据。"


if __name__ == "__main__":
    print(explain("投递、复盘和持续学习"))
