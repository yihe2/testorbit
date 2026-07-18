import json
from pathlib import Path

from testorbit.history import (
    TaskStats,
    aggregate_task_stats,
    append_run_result,
    export_run_history,
    filter_run_history,
    flaky_task_names,
    latest_run_for_task,
    read_run_history,
    summarize_run_history,
    task_failure_counts,
    task_run_counts,
)
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
        "status": "passed",
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


def test_filter_run_history_by_status() -> None:
    records = [
        {"task_name": "unit", "status": "passed"},
        {"task_name": "smoke", "status": "failed"},
    ]

    assert filter_run_history(records, "failed") == [{"task_name": "smoke", "status": "failed"}]


def test_latest_run_for_task_returns_most_recent_match() -> None:
    records = [
        {"task_name": "unit", "status": "failed", "exit_code": 1},
        {"task_name": "smoke", "status": "passed", "exit_code": 0},
        {"task_name": "unit", "status": "passed", "exit_code": 0},
    ]

    assert latest_run_for_task(records, "unit") == {
        "task_name": "unit",
        "status": "passed",
        "exit_code": 0,
    }


def test_latest_run_for_task_returns_none_when_missing() -> None:
    assert latest_run_for_task([{"task_name": "unit", "status": "passed"}], "smoke") is None


def test_export_run_history_writes_json_array(tmp_path: Path) -> None:
    export_path = tmp_path / "exports" / "runs.json"
    records = [{"task_name": "unit", "status": "passed"}]

    export_run_history(records, export_path)

    assert export_path.read_text(encoding="utf-8") == '[\n  {\n    "status": "passed",\n    "task_name": "unit"\n  }\n]'


def test_task_failure_counts_ignores_passing_runs() -> None:
    records = [
        {"task_name": "unit", "status": "failed", "exit_code": 1},
        {"task_name": "unit", "status": "passed", "exit_code": 0},
        {"task_name": "unit", "status": "failed", "exit_code": 1},
        {"task_name": "smoke", "status": "passed", "exit_code": 0},
    ]

    assert task_failure_counts(records) == {"unit": 2}


def test_task_failure_counts_uses_exit_code_when_status_missing() -> None:
    records = [
        {"task_name": "api", "exit_code": 1},
        {"task_name": "api", "exit_code": 1},
        {"task_name": "unit", "exit_code": 0},
    ]

    assert task_failure_counts(records) == {"api": 2}


def test_flaky_task_names_marks_repeated_failures() -> None:
    records = [
        {"task_name": "unit", "status": "failed", "exit_code": 1},
        {"task_name": "unit", "status": "failed", "exit_code": 1},
        {"task_name": "smoke", "status": "failed", "exit_code": 1},
        {"task_name": "api", "status": "passed", "exit_code": 0},
    ]

    assert flaky_task_names(records) == ["unit"]


def test_flaky_task_names_respects_threshold() -> None:
    records = [
        {"task_name": "smoke", "status": "failed", "exit_code": 1},
        {"task_name": "smoke", "status": "failed", "exit_code": 1},
    ]

    assert flaky_task_names(records, threshold=3) == []
    assert flaky_task_names(records, threshold=2) == ["smoke"]


def test_task_run_counts_includes_passing_and_failing_runs() -> None:
    records = [
        {"task_name": "unit", "status": "passed", "exit_code": 0},
        {"task_name": "unit", "status": "failed", "exit_code": 1},
        {"task_name": "smoke", "status": "passed", "exit_code": 0},
    ]

    assert task_run_counts(records) == {"unit": 2, "smoke": 1}


def test_history_aggregation_is_empty_for_no_records() -> None:
    assert task_run_counts([]) == {}
    assert task_failure_counts([]) == {}
    assert flaky_task_names([]) == []
    assert aggregate_task_stats([]) == []


def test_aggregate_task_stats_combines_runs_and_failures() -> None:
    records = [
        {"task_name": "unit", "status": "passed", "exit_code": 0},
        {"task_name": "unit", "status": "failed", "exit_code": 1},
        {"task_name": "unit", "status": "failed", "exit_code": 1},
        {"task_name": "smoke", "status": "passed", "exit_code": 0},
    ]

    assert aggregate_task_stats(records) == [
        TaskStats(task_name="smoke", runs=1, failed=0),
        TaskStats(task_name="unit", runs=3, failed=2),
    ]
    assert aggregate_task_stats(records)[1].is_flaky()
    assert not aggregate_task_stats(records)[0].is_flaky()


def test_missing_task_names_are_grouped_as_unknown() -> None:
    records = [
        {"exit_code": 1},
        {"task_name": "", "status": "failed", "exit_code": 1},
    ]

    assert task_failure_counts(records) == {"(unknown)": 2}
    assert flaky_task_names(records) == ["(unknown)"]


def test_explicit_passed_status_is_not_a_failure() -> None:
    records = [{"task_name": "unit", "status": "passed", "exit_code": 1}]

    assert summarize_run_history(records)["failed"] == 0
    assert task_failure_counts(records) == {}
    assert flaky_task_names(records) == []


def test_single_failure_is_not_flaky() -> None:
    assert flaky_task_names([{"task_name": "unit", "status": "failed", "exit_code": 1}]) == []
