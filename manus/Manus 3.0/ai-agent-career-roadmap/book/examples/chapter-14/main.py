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
