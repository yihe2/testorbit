from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml
from rich.console import Console

console = Console()


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


def version() -> int:
    console.print("TestOrbit 0.1.0")
    return 0


def doctor(config: Path) -> int:
    data = load_config(config)
    tasks = get_tasks(data)
    validate_tasks(tasks)

    console.print(f"Config loaded from {config}")
    console.print(f"Discovered {len(tasks)} task(s)")
    return 0


def list_tasks(config: Path) -> int:
    data = load_config(config)
    tasks = get_tasks(data)

    if not tasks:
        console.print("No tasks configured.")
        return 0

    console.print("Configured tasks:")
    for task_name in sorted(tasks):
        console.print(f"- {task_name}")
    return 0


def show_task(config: Path, task_name: str) -> int:
    data = load_config(config)
    tasks = get_tasks(data)

    task = tasks.get(task_name)
    if not isinstance(task, dict):
        raise ValueError(f"Task not found: {task_name}")

    console.print(f"Task: {task_name}")
    for key, value in task.items():
        console.print(f"{key}: {value}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="testorbit", description="Run and manage test tasks from one simple CLI.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("version", help="Show the current TestOrbit version.")

    doctor_parser = subparsers.add_parser("doctor", help="Validate the config file and show detected tasks.")
    doctor_parser.add_argument("--config", "-c", default="testorbit.yml")

    list_parser = subparsers.add_parser("list", help="List configured test tasks.")
    list_parser.add_argument("--config", "-c", default="testorbit.yml")

    show_parser = subparsers.add_parser("show", help="Show details for one configured test task.")
    show_parser.add_argument("task_name")
    show_parser.add_argument("--config", "-c", default="testorbit.yml")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "version":
            return version()
        if args.command == "doctor":
            return doctor(Path(args.config))
        if args.command == "list":
            return list_tasks(Path(args.config))
        if args.command == "show":
            return show_task(Path(args.config), args.task_name)
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        return 1

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
