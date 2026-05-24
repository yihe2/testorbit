import json
from pathlib import Path

from testorbit.history import append_run_result
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
