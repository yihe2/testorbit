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
