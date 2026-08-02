# Architecture Notes

TestOrbit is intentionally small, but the code should still keep a few clear boundaries.

## CLI Layer

`testorbit.cli` owns argument parsing, config lookup, user-facing messages, and exit codes.

## Runner Layer

`testorbit.runner` owns command parsing, executable lookup, subprocess startup, and structured results. Missing tools and OS start failures are mapped to `ValueError` so the CLI can print a clear message without writing history.

Run results expose a small dictionary representation so future history and report features can reuse the same shape.

## Config Layer

`testorbit.config` owns YAML loading, `tasks` mapping checks, and per-task command validation. The CLI asks this module for a config dictionary, then looks up task names for `list`, `show`, `run`, and `doctor`.

Task discovery is a config lookup, not a filesystem walk. The flow is documented in [task-discovery.md](task-discovery.md).

## Report Layer

`testorbit.report` turns run-history records into a `ReportSummary` and renders `templates/summary.html.j2` with Jinja2. Default artifacts land in `reports/`, which is gitignored. CI jobs can also write history to `reports/runs.jsonl` so one folder upload has the JSONL log, JSON export, and HTML page. Usage notes live in [reports.md](reports.md) and [ci.md](ci.md).

## Near-Term Direction

- capture command output when useful
- add retry and flaky-test tracking next
- keep subprocess behavior isolated behind runner tests
