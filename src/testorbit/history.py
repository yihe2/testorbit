from __future__ import annotations

import json
from pathlib import Path

from testorbit.runner import RunResult


def append_run_result(history_path: Path, result: RunResult) -> None:
    history_path.parent.mkdir(parents=True, exist_ok=True)

    with history_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(result.to_dict(), sort_keys=True))
        handle.write("\n")


def read_run_history(history_path: Path) -> list[dict]:
    if not history_path.exists():
        return []

    records = []
    for line in history_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def summarize_run_history(records: list[dict]) -> dict:
    total = len(records)
    failed = sum(1 for record in records if record.get("status") == "failed" or record.get("exit_code", 1) != 0)
    passed = total - failed

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
    }


def filter_run_history(records: list[dict], status: str | None = None) -> list[dict]:
    if status is None:
        return records

    return [record for record in records if record.get("status") == status]


def export_run_history(records: list[dict], export_path: Path) -> None:
    export_path.parent.mkdir(parents=True, exist_ok=True)
    export_path.write_text(json.dumps(records, indent=2, sort_keys=True), encoding="utf-8")
