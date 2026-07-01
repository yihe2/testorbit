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


def starter_config() -> dict:
    return {
        "tasks": {
            "unit": {
                "runner": "pytest",
                "command": "pytest tests",
                "tags": ["fast", "local"],
            },
            "smoke": {
                "runner": "pytest",
                "command": "pytest -m smoke",
                "tags": ["smoke", "focused"],
            },
            "api": {
                "runner": "pytest",
                "command": "pytest tests/api",
                "tags": ["api", "integration"],
            },
        }
    }


def write_starter_config(config_path: Path) -> Path:
    if config_path.exists():
        raise ValueError(f"Config file already exists: {config_path}")

    data = starter_config()
    validate_tasks(get_tasks(data))

    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        yaml.safe_dump(data, sort_keys=False),
        encoding="utf-8",
    )

    loaded = load_config(config_path)
    validate_tasks(get_tasks(loaded))
    return config_path
