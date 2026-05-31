from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml
from rich.console import Console

from testorbit.history import append_run_result, read_run_history, summarize_run_history
from testorbit.runner import execute_command

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


def run_task(config: Path, task_name: str, dry_run: bool, history_path: Path) -> int:
    data = load_config(config)
    tasks = get_tasks(data)

    task = tasks.get(task_name)
    if not isinstance(task, dict):
        raise ValueError(f"Task not found: {task_name}")

    command = task.get("command")
    if not command:
        raise ValueError(f"Task '{task_name}' must define a command.")

    if dry_run:
        console.print(f"Would run: {command}")
        return 0

    console.print(f"Running task '{task_name}': {command}")
    result = execute_command(task_name, command)
    append_run_result(history_path, result)
    console.print(f"Finished in {result.duration_seconds:.2f}s")
    return result.exit_code


def show_history(history_path: Path, limit: int) -> int:
    if limit < 1:
        raise ValueError("History limit must be at least 1.")

    records = read_run_history(history_path)
    if not records:
        console.print("No run history found.")
        return 0

    summary = summarize_run_history(records)
    console.print(
        f"Runs: {summary['total']} total, "
        f"{summary['passed']} passed, {summary['failed']} failed"
    )

    for record in records[-limit:]:
        console.print(
            f"{record['task_name']} exit={record['exit_code']} "
            f"duration={record['duration_seconds']}s"
        )
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

    run_parser = subparsers.add_parser("run", help="Run one configured test task.")
    run_parser.add_argument("task_name")
    run_parser.add_argument("--config", "-c", default="testorbit.yml")
    run_parser.add_argument("--dry-run", action="store_true", help="Print the command without executing it.")
    run_parser.add_argument("--history-path", default="run-history/runs.jsonl", help="Where run metadata is stored.")

    history_parser = subparsers.add_parser("history", help="Show recent task run records.")
    history_parser.add_argument("--history-path", default="run-history/runs.jsonl", help="Where run metadata is stored.")
    history_parser.add_argument("--limit", type=int, default=5, help="Maximum records to show.")

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
        if args.command == "run":
            return run_task(Path(args.config), args.task_name, args.dry_run, Path(args.history_path))
        if args.command == "history":
            return show_history(Path(args.history_path), args.limit)
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        return 1

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
