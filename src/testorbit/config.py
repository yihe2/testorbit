from __future__ import annotations

from pathlib import Path

import yaml

DEFAULT_CONFIG_PATH = Path("testorbit.yml")
QUARANTINE_KEY = "quarantine"


def get_tasks(data: dict) -> dict:
    tasks = data.get("tasks", {})

    if not isinstance(tasks, dict):
        raise ValueError("'tasks' must be a mapping of task names to command definitions.")

    return tasks


def validate_tasks(tasks: dict) -> None:
    for task_name, task in tasks.items():
        if not isinstance(task, dict):
            raise ValueError(f"Task '{task_name}' must be a mapping.")
        task_command(task, task_name)


def task_command(task: dict, task_name: str) -> str:
    command = task.get("command")
    if not isinstance(command, str) or not command.strip():
        raise ValueError(f"Task '{task_name}' must define a command.")
    return command.strip()


def get_quarantine(data: dict) -> list[str]:
    raw = data.get(QUARANTINE_KEY, [])
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise ValueError("'quarantine' must be a list of task names.")

    names = []
    for item in raw:
        if not isinstance(item, str) or not item.strip():
            raise ValueError("Quarantine entries must be non-empty task names.")
        names.append(item.strip())
    return names


def validate_quarantine(tasks: dict, quarantine: list[str]) -> None:
    unknown = [name for name in quarantine if name not in tasks]
    if unknown:
        raise ValueError("Unknown quarantined task(s): " + ", ".join(unknown))


def resolve_quarantine(data: dict, tasks: dict) -> list[str]:
    quarantine = get_quarantine(data)
    validate_quarantine(tasks, quarantine)
    return quarantine


def is_quarantined(task_name: str, quarantine: list[str]) -> bool:
    return task_name in quarantine


def load_config(config_path: Path) -> dict:
    if not config_path.exists():
        raise ValueError(f"Config file not found: {config_path}")

    try:
        with config_path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML in {config_path}.") from exc

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
