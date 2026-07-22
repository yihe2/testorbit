from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rich.console import Console

from testorbit import __version__
from testorbit.config import (
    DEFAULT_CONFIG_PATH,
    get_quarantine,
    get_tasks,
    load_config,
    validate_quarantine,
    validate_tasks,
    write_starter_config,
)
from testorbit.history import (
    DEFAULT_HISTORY_PATH,
    append_run_result,
    export_run_history,
    filter_run_history,
    flaky_task_names,
    latest_run_for_task,
    read_run_history,
    summarize_run_history,
)
from testorbit.report import DEFAULT_EXPORT_PATH, DEFAULT_REPORT_PATH, build_report, render_html_report
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


def version() -> int:
    console.print(f"TestOrbit {__version__}")
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
    quarantine = get_quarantine(data)
    validate_quarantine(tasks, quarantine)

    task = tasks.get(task_name)
    if not isinstance(task, dict):
        raise ValueError(f"Task not found: {task_name}")

    command = task.get("command")
    if not command:
        raise ValueError(f"Task '{task_name}' must define a command.")

    if task_name in quarantine:
        console.print(f"[yellow]Skipping quarantined task '{task_name}'[/yellow]")
        return 0

    if dry_run:
        console.print(f"Would run: {command}")
        return 0

    console.print(f"Running task '{task_name}': {command}")
    result = execute_command(task_name, command)
    append_run_result(history_path, result)
    if result.status == "passed":
        console.print(f"[green]Task '{task_name}' passed[/green]")
    else:
        console.print(f"[red]Task '{task_name}' failed with exit {result.exit_code}[/red]")
    console.print(f"Finished in {result.duration_seconds:.2f}s")
    return result.exit_code


def require_status(status: str | None) -> str | None:
    if status not in {None, "passed", "failed"}:
        raise ValueError("History status must be 'passed' or 'failed'.")
    return status


def show_history(history_path: Path, limit: int, status: str | None) -> int:
    require_status(status)
    if limit < 1:
        raise ValueError("History limit must be at least 1.")

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
    flaky = flaky_task_names(records)
    if flaky:
        console.print("Flaky: " + ", ".join(flaky))

    for record in records[-limit:]:
        console.print(
            f"{record['task_name']} exit={record['exit_code']} "
            f"duration={record['duration_seconds']}s"
        )
    return 0


def export_history(history_path: Path, export_path: Path, status: str | None) -> int:
    records = filter_run_history(read_run_history(history_path), require_status(status))
    export_run_history(records, export_path)
    console.print(f"Exported {len(records)} record(s) to {export_path}")
    return 0


def write_report(history_path: Path, output_path: Path, status: str | None) -> int:
    written = render_html_report(build_report(history_path, require_status(status)), output_path)
    resolved = written.resolve()
    console.print(f"Wrote report to {resolved}")
    console.print(f"Open {resolved.as_uri()}")
    return 0


def init_config(config_path: Path, force: bool = False) -> int:
    if config_path.exists() and force:
        config_path.unlink()

    written = write_starter_config(config_path)
    tasks = get_tasks(load_config(written))
    console.print(f"Created {written} with {len(tasks)} task(s).")
    console.print("Next:")
    console.print(f"  testorbit doctor --config {written}")
    console.print(f"  testorbit list --config {written}")
    console.print(f"  testorbit run unit --dry-run --config {written}")
    return 0


def add_config_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--config",
        "-c",
        default=str(DEFAULT_CONFIG_PATH),
        help="YAML file that defines named test tasks.",
    )


def add_history_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--history-path",
        default=str(DEFAULT_HISTORY_PATH),
        help="JSONL file used to store and read task run history.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="testorbit",
        description="Initialize a project, then run and summarize saved test tasks.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("version", help="Print the installed TestOrbit version.")

    init_parser = subparsers.add_parser("init", help="Create a starter testorbit.yml in the current directory.")
    init_parser.add_argument(
        "--config",
        "-c",
        default=str(DEFAULT_CONFIG_PATH),
        help="Path to write the starter config file.",
    )
    init_parser.add_argument("--force", action="store_true", help="Overwrite an existing config file.")

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
    export_parser.add_argument(
        "--output",
        default=str(DEFAULT_EXPORT_PATH),
        help="JSON file to write. Defaults to reports/runs.json.",
    )
    export_parser.add_argument("--status", choices=["passed", "failed"], help="Only export records with this status.")

    report_parser = subparsers.add_parser("report", help="Render an HTML summary of task run history.")
    add_history_argument(report_parser)
    report_parser.add_argument(
        "--output",
        default=str(DEFAULT_REPORT_PATH),
        help="HTML file to write. Defaults to reports/summary.html.",
    )
    report_parser.add_argument("--status", choices=["passed", "failed"], help="Only include records with this status.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "version":
            return version()
        if args.command == "init":
            return init_config(Path(args.config), args.force)
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
        if args.command == "report":
            return write_report(Path(args.history_path), Path(args.output), args.status)
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        return 1

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
