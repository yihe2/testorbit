import json
from pathlib import Path

from testorbit.history import append_run_result, read_run_history, summarize_run_history
from testorbit.runner import RunResult


def test_append_run_result_writes_json_line(tmp_path: Path) -> None:
    history_path = tmp_path / "run-history" / "runs.jsonl"
    result = RunResult("unit", "pytest tests", 0, 0.42)

    append_run_result(history_path, result)

    lines = history_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0]) == {
        "command": "pytest tests",
        "duration_seconds": 0.42,
        "exit_code": 0,
        "task_name": "unit",
    }


def test_read_run_history_returns_records(tmp_path: Path) -> None:
    history_path = tmp_path / "runs.jsonl"
    append_run_result(history_path, RunResult("unit", "pytest tests", 0, 0.42))
    append_run_result(history_path, RunResult("smoke", "pytest -m smoke", 1, 1.25))

    records = read_run_history(history_path)

    assert [record["task_name"] for record in records] == ["unit", "smoke"]


def test_read_run_history_returns_empty_list_for_missing_file(tmp_path: Path) -> None:
    assert read_run_history(tmp_path / "missing.jsonl") == []


def test_summarize_run_history_counts_passed_and_failed_runs() -> None:
    records = [
        {"task_name": "unit", "exit_code": 0},
        {"task_name": "smoke", "exit_code": 1},
        {"task_name": "api", "exit_code": 0},
    ]

    assert summarize_run_history(records) == {
        "total": 3,
        "passed": 2,
        "failed": 1,
    }
