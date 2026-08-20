"""Dependency-free checks for the daily scaffold."""

from starter import TOPIC, build_task_context


def test_valid_context() -> None:
    context = build_task_context(TOPIC, "output/result.json")
    assert context.topic
    assert context.output_path == "output/result.json"


def test_empty_topic_is_rejected() -> None:
    try:
        build_task_context("   ", "output/result.json")
    except ValueError as exc:
        assert "topic" in str(exc)
    else:
        raise AssertionError("empty topic should be rejected")


if __name__ == "__main__":
    test_valid_context()
    test_empty_topic_is_rejected()
    print("starter checks passed")
