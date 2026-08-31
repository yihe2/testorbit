# Backlog

This backlog captures the first set of product questions and candidate tasks for TestOrbit.

## Core Questions

- how should named test tasks be represented in config
- should retries happen at the task level or failed-test level
- what metadata is useful enough to store after each run
- how much reporting is needed for the MVP

## Shipped In 1.0

- named task config and `doctor`
- `run` with history, JSON export, and HTML reports
- GitHub Actions example workflow
- flaky-task heuristics
- quarantine list support
- demo project under `examples/demo`

## After 1.0

See [post-release.md](post-release.md) for retry, include/exclude, duration trends, and related follow-ups.

## Cut For 1.0

- optional secondary adapter for JavaScript test commands
