from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class RunResult:
    task_name: str
    command: str
    exit_code: int
    duration_seconds: float


def execute_command(task_name: str, command: str) -> RunResult:
    started_at = time.perf_counter()
    completed = subprocess.run(command, shell=True, check=False)
    duration_seconds = time.perf_counter() - started_at
    return RunResult(
        task_name=task_name,
        command=command,
        exit_code=completed.returncode,
        duration_seconds=duration_seconds,
    )
