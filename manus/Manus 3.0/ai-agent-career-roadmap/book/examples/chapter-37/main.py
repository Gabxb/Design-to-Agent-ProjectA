"""Chapter 37 teaching example: 条件分支与循环."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


State = Literal["pending", "needs_approval", "completed", "failed"]


@dataclass(frozen=True)
class WorkflowResult:
    state: State
    message: str


def advance(state: State, approved: bool) -> WorkflowResult:
    if state == "pending":
        return WorkflowResult("needs_approval", "等待人工确认")
    if state == "needs_approval" and approved:
        return WorkflowResult("completed", "已完成受控步骤")
    if state == "needs_approval":
        return WorkflowResult("failed", "未获批准，未执行副作用操作")
    return WorkflowResult(state, "状态不再推进")


if __name__ == "__main__":
    waiting = advance("pending", False)
    print(waiting)
    print(advance(waiting.state, True))
