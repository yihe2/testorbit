# Early Backlog

This backlog captures the first set of product questions and candidate tasks for TestOrbit.

## Core Questions

- how should named test tasks be represented in config
- should retries happen at the task level or failed-test level
- what metadata is useful enough to store after each run
- how much reporting is needed for the MVP

## MVP Backlog

- define config schema for named tasks
- support a `doctor` command for config validation
- add a `run` command for task execution
- record run status, duration, and command used
- generate JSON summaries before HTML reports

## Nice-To-Have Backlog

- flaky-test heuristics
- quarantine list support
- GitHub Actions example workflow
- optional secondary adapter for JavaScript test commands
