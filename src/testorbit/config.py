from __future__ import annotations

from pathlib import Path

import yaml

DEFAULT_CONFIG_PATH = Path("testorbit.yml")


def get_tasks(data: dict) -> dict:
    tasks = data.get("tasks", {})

    if not isinstance(tasks, dict):
        raise ValueError("'tasks' must be a mapping of task names to command definitions.")

    return tasks


def validate_tasks(tasks: dict) -> None:
    for task_name, task in tasks.items():
        if not isinstance(task, dict):
            raise ValueError(f"Task '{task_name}' must be a mapping.")
        if not task.get("command"):
            raise ValueError(f"Task '{task_name}' must define a command.")


def load_config(config_path: Path) -> dict:
    if not config_path.exists():
        raise ValueError(f"Config file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    if not isinstance(data, dict):
        raise ValueError("Config file must contain a mapping at the top level.")

    return data
