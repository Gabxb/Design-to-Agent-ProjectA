"""Runnable scaffold for W18-D02: 可观测性、成本与性能：基础编码练习."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path


TASK_ID = "W18-D02"
TOPIC = "可观测性、成本与性能：基础编码练习"


@dataclass(frozen=True)
class TaskContext:
    task_id: str
    topic: str
    output_path: str


def build_task_context(topic: str, output_path: str) -> TaskContext:
    cleaned_topic = " ".join(topic.strip().split())
    if not cleaned_topic:
        raise ValueError("topic must not be empty")
    path = Path(output_path)
    if path.is_absolute():
        raise ValueError("output_path must be project-relative")
    return TaskContext(task_id=TASK_ID, topic=cleaned_topic, output_path=path.as_posix())


def main() -> None:
    context = build_task_context(TOPIC, "output/result.json")
    print(json.dumps(asdict(context), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
