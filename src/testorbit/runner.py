from __future__ import annotations

import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class RunResult:
    task_name: str
    command: str
    exit_code: int


def execute_command(task_name: str, command: str) -> RunResult:
    completed = subprocess.run(command, shell=True, check=False)
    return RunResult(task_name=task_name, command=command, exit_code=completed.returncode)
