from __future__ import annotations

KNOWN_RUNNERS = {
    "pytest": "pytest",
    "npm": "npm test",
    "npm-test": "npm test",
    "jest": "npx jest",
}


def build_task_command(task: dict, task_name: str) -> str:
    command = task.get("command")
    if isinstance(command, str) and command.strip():
        return command.strip()

    runner = str(task.get("runner") or "").strip().lower()
    default = KNOWN_RUNNERS.get(runner)
    if default:
        return default

    raise ValueError(
        f"Task '{task_name}' must define a command, or a known runner (pytest, npm, jest)."
    )
