# Architecture Notes

TestOrbit is intentionally small, but the code should still keep a few clear boundaries.

## CLI Layer

`testorbit.cli` owns argument parsing, config lookup, user-facing messages, and exit codes.

## Runner Layer

`testorbit.runner` owns command parsing, executable lookup, subprocess startup, and structured results. Missing tools and OS start failures are mapped to `ValueError` so the CLI can print a clear message without writing history.

Run results expose a small dictionary representation so future history and report features can reuse the same shape.

## Config Layer

`testorbit.config` owns YAML loading, `tasks` mapping checks, and per-task command lookup via `task_command`. The CLI asks this module for a config dictionary, then looks up task names for `list`, `show`, `run`, and `doctor`.

Task discovery is a config lookup, not a filesystem walk. The flow is documented in [task-discovery.md](task-discovery.md).

`command` is what executes. `runner` is an optional label only. A Week 16 spike that defaulted commands from `runner: npm` was cut; see [adapters.md](adapters.md).

## Report Layer

`testorbit.report` turns run-history records into a `ReportSummary` and renders `templates/summary.html.j2` with Jinja2. Default artifacts land in `reports/`, which is gitignored. CI jobs can also write history to `reports/runs.jsonl` so one folder upload has the JSONL log, JSON export, and HTML page. Usage notes live in [reports.md](reports.md) and [ci.md](ci.md).

## 1.0 Shape

The CLI, config, runner, history, and report layers above are the 1.0 surface. Keep subprocess behavior isolated behind runner tests. Ideas that missed 1.0 are in [post-release.md](post-release.md).
