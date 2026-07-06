from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RunResult:
    task_name: str
    command: str
    exit_code: int
    duration_seconds: float

    @property
    def status(self) -> str:
        return "passed" if self.exit_code == 0 else "failed"

    def to_dict(self) -> dict:
        return {
            "task_name": self.task_name,
            "command": self.command,
            "exit_code": self.exit_code,
            "status": self.status,
            "duration_seconds": round(self.duration_seconds, 3),
        }


def command_executable(command: str) -> str:
    parts = shlex.split(command, posix=os.name != "nt")
    if not parts:
        raise ValueError("Task command is empty.")
    return parts[0]


def require_command_executable(command: str) -> str:
    executable = command_executable(command)
    if os.path.sep in executable or (os.name == "nt" and len(executable) >= 3 and executable[1] == ":"):
        path = Path(executable)
        if not path.exists():
            raise ValueError(f"Command not found: {executable}")
        return str(path)

    resolved = shutil.which(executable)
    if resolved is None:
        raise ValueError(f"Command not found: {executable}")
    return resolved


def execute_command(task_name: str, command: str) -> RunResult:
    require_command_executable(command)
    started_at = time.perf_counter()
    completed = subprocess.run(command, shell=True, check=False)
    duration_seconds = time.perf_counter() - started_at
    return RunResult(
        task_name=task_name,
        command=command,
        exit_code=completed.returncode,
        duration_seconds=duration_seconds,
    )
