# Early Backlog

This backlog captures the first set of product questions and candidate tasks for TestOrbit.

## Core Questions

- how should named test tasks be represented in config
- should retries happen at the task level or failed-test level
- what metadata is useful enough to store after each run
- how much reporting is needed for the MVP

## Shipped

- named task config and `doctor`
- `run` with history, JSON export, and HTML reports
- GitHub Actions example workflow
- flaky-task heuristics
- quarantine list support
- demo project under `examples/demo`

## Still Open

- retries at the task or failed-test level
- include/exclude filters
- optional secondary adapter for JavaScript test commands
