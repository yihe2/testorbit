from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml
from rich.console import Console

from testorbit.history import (
    append_run_result,
    export_run_history,
    filter_run_history,
    latest_run_for_task,
    read_run_history,
    summarize_run_history,
)
from testorbit.runner import execute_command

console = Console()


def format_last_run(record: dict | None, prefix: str = "last=") -> str:
    if record is None:
        return f"{prefix}none"

    status = record.get("status")
    if status not in {"passed", "failed"}:
        status = "passed" if record.get("exit_code", 1) == 0 else "failed"

    duration = record.get("duration_seconds")
    if duration is None:
        return f"{prefix}{status}"
    return f"{prefix}{status} ({duration}s)"


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


def list_tasks(config: Path, history_path: Path) -> int:
    data = load_config(config)
    tasks = get_tasks(data)

    if not tasks:
        console.print("No tasks configured.")
        return 0

    records = read_run_history(history_path)
    console.print("Configured tasks:")
    for task_name in sorted(tasks):
        if records:
            console.print(f"- {task_name} {format_last_run(latest_run_for_task(records, task_name))}")
        else:
            console.print(f"- {task_name}")
    return 0


def show_task(config: Path, task_name: str, history_path: Path) -> int:
    data = load_config(config)
    tasks = get_tasks(data)

    task = tasks.get(task_name)
    if not isinstance(task, dict):
        raise ValueError(f"Task not found: {task_name}")

    console.print(f"Task: {task_name}")
    for key, value in task.items():
        console.print(f"{key}: {value}")
    last_run = latest_run_for_task(read_run_history(history_path), task_name)
    console.print(format_last_run(last_run, prefix="Last run: "))
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


def show_history(history_path: Path, limit: int, status: str | None) -> int:
    if limit < 1:
        raise ValueError("History limit must be at least 1.")
    if status not in {None, "passed", "failed"}:
        raise ValueError("History status must be 'passed' or 'failed'.")

    records = read_run_history(history_path)
    records = filter_run_history(records, status)
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


def export_history(history_path: Path, export_path: Path, status: str | None) -> int:
    if status not in {None, "passed", "failed"}:
        raise ValueError("History status must be 'passed' or 'failed'.")

    records = filter_run_history(read_run_history(history_path), status)
    export_run_history(records, export_path)
    console.print(f"Exported {len(records)} record(s) to {export_path}")
    return 0


def add_config_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--config",
        "-c",
        default="testorbit.yml",
        help="YAML file that defines named test tasks.",
    )


def add_history_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--history-path",
        default="run-history/runs.jsonl",
        help="JSONL file used to store and read task run history.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="testorbit",
        description="Run, inspect, and summarize saved test tasks from one CLI.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("version", help="Print the installed TestOrbit version.")

    doctor_parser = subparsers.add_parser("doctor", help="Validate a config file and count discovered tasks.")
    add_config_argument(doctor_parser)

    list_parser = subparsers.add_parser("list", help="List configured tasks and their last run status.")
    add_config_argument(list_parser)
    add_history_argument(list_parser)

    show_parser = subparsers.add_parser("show", help="Show one task's command, metadata, and last run.")
    show_parser.add_argument("task_name", help="Name of the task defined in the config file.")
    add_config_argument(show_parser)
    add_history_argument(show_parser)

    run_parser = subparsers.add_parser("run", help="Execute one configured task and record the result.")
    run_parser.add_argument("task_name", help="Name of the task defined in the config file.")
    add_config_argument(run_parser)
    run_parser.add_argument("--dry-run", action="store_true", help="Print the command without executing it.")
    add_history_argument(run_parser)

    history_parser = subparsers.add_parser("history", help="Show a pass/fail summary of recent task runs.")
    add_history_argument(history_parser)
    history_parser.add_argument("--limit", type=int, default=5, help="Maximum number of recent records to print.")
    history_parser.add_argument("--status", choices=["passed", "failed"], help="Only show records with this status.")

    export_parser = subparsers.add_parser("export-history", help="Write filtered run history to a JSON file.")
    add_history_argument(export_parser)
    export_parser.add_argument("--output", required=True, help="JSON file to write.")
    export_parser.add_argument("--status", choices=["passed", "failed"], help="Only export records with this status.")

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
            return list_tasks(Path(args.config), Path(args.history_path))
        if args.command == "show":
            return show_task(Path(args.config), args.task_name, Path(args.history_path))
        if args.command == "run":
            return run_task(Path(args.config), args.task_name, args.dry_run, Path(args.history_path))
        if args.command == "history":
            return show_history(Path(args.history_path), args.limit, args.status)
        if args.command == "export-history":
            return export_history(Path(args.history_path), Path(args.output), args.status)
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        return 1

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
