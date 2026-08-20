from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from testorbit.runner import RunResult

DEFAULT_HISTORY_PATH = Path("run-history/runs.jsonl")
DEFAULT_FLAKY_THRESHOLD = 2


def _record_status(record: dict) -> str:
    status = record.get("status")
    if status in {"passed", "failed"}:
        return status
    return "passed" if record.get("exit_code", 1) == 0 else "failed"


def _record_failed(record: dict) -> bool:
    return _record_status(record) == "failed"


@dataclass(frozen=True)
class TaskStats:
    task_name: str
    runs: int
    failed: int

    @property
    def passed(self) -> int:
        return self.runs - self.failed

    def is_flaky(self, threshold: int = DEFAULT_FLAKY_THRESHOLD) -> bool:
        return self.failed >= threshold


def append_run_result(history_path: Path, result: RunResult) -> None:
    history_path.parent.mkdir(parents=True, exist_ok=True)

    with history_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(result.to_dict(), sort_keys=True))
        handle.write("\n")


def read_run_history(history_path: Path) -> list[dict]:
    if not history_path.exists():
        return []

    records = []
    for line_number, line in enumerate(history_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSONL in {history_path} on line {line_number}.") from exc
    return records


def summarize_run_history(records: list[dict]) -> dict:
    total = len(records)
    failed = sum(1 for record in records if _record_failed(record))
    passed = total - failed

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
    }


def task_failure_counts(records: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        failed = _record_failed(record)
        if not failed:
            continue
        task_name = record.get("task_name") or "(unknown)"
        counts[task_name] = counts.get(task_name, 0) + 1
    return counts


def flaky_task_names(records: list[dict], threshold: int = DEFAULT_FLAKY_THRESHOLD) -> list[str]:
    return [stats.task_name for stats in aggregate_task_stats(records) if stats.is_flaky(threshold)]


def task_run_counts(records: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        task_name = record.get("task_name") or "(unknown)"
        counts[task_name] = counts.get(task_name, 0) + 1
    return counts


def aggregate_task_stats(records: list[dict]) -> list[TaskStats]:
    runs = task_run_counts(records)
    failed = task_failure_counts(records)
    return [
        TaskStats(task_name=name, runs=runs.get(name, 0), failed=failed.get(name, 0))
        for name in sorted(set(runs) | set(failed))
    ]


def filter_run_history(records: list[dict], status: str | None = None) -> list[dict]:
    if status is None:
        return list(records)

    return [record for record in records if _record_status(record) == status]


def latest_run_for_task(records: list[dict], task_name: str) -> dict | None:
    for record in reversed(records):
        if record.get("task_name") == task_name:
            return record
    return None


def export_run_history(records: list[dict], export_path: Path) -> None:
    export_path.parent.mkdir(parents=True, exist_ok=True)
    export_path.write_text(json.dumps(records, indent=2, sort_keys=True), encoding="utf-8")
