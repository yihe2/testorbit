# Changelog

## 1.0.0 — 2026-08-31

First stable release of TestOrbit.

- load named tasks from `testorbit.yml`
- `init`, `doctor`, `list`, `show`, and `run`
- JSONL run history, `history`, and `export-history`
- HTML summary reports with flaky-task hints
- optional `quarantine` list that skips tasks without deleting them
- `--ci` output for GitHub Actions, with artifacts under `reports/`
- demo project in `examples/demo`

Not included: include/exclude filters, failed-test retry, duration trends, and a first-class npm adapter. `command: npm test` still runs through the shell runner.
