# TestOrbit

TestOrbit is a lightweight test automation helper for developers who want one clean command to run, filter, retry, and report on their test suites.

This project is scoped as a 4-month GitHub portfolio build from **May 1, 2026** to **August 31, 2026**. The goal is to ship a realistic, polished CLI product with strong documentation, clean commit history, and a visible progression from MVP to release candidate.

## Project Goal

Build a Python-based CLI tool that makes local test execution easier by:

- loading saved test commands from a config file
- running targeted test groups with simple aliases
- retrying failed tests
- collecting JSON run history
- generating a readable HTML summary report
- preparing teams for CI adoption with GitHub Actions examples

## Why This Scope Works

The time window covers about **18 calendar weeks**. With a target of **8-10 commits per week**, the full project should land around **150-170 commits**, which is enough to show consistent work without forcing fake micro-commits.

To keep the project finishable, the MVP focuses on:

- one primary runtime: Python 3.11+
- one polished CLI
- one real adapter first: `pytest`
- one generic fallback adapter for shell commands
- lightweight reporting instead of a full web app

## Final Feature Scope

### Must Ship

- CLI entrypoint: `testorbit`
- YAML config file support
- named test tasks such as `smoke`, `unit`, `api`
- include/exclude filters
- failed-test retry flow
- run history stored locally
- JSON export
- HTML report generation
- GitHub Actions sample workflow
- unit tests for the core orchestration logic

### Nice To Have If Time Remains

- flaky-test tagging
- quarantine list support
- duration trend summaries
- adapter for `npm test` / `jest`
- colored terminal output themes

### Explicitly Out Of Scope

- cloud sync
- database-backed dashboard
- browser UI app
- parallel distributed execution across machines
- enterprise test management integrations

## Recommended Tech Stack

- Python 3.11+
- `argparse` for the initial CLI, with the option to migrate to `typer` later if the project benefits from richer command UX
- `PyYAML` for config loading
- `rich` for terminal output
- `jinja2` for HTML reports
- `pytest` for automated tests

## Repository Shape

```text
testorbit/
  src/testorbit/
  tests/
  docs/
  README.md
  pyproject.toml
```

## Commit Rhythm

Use **4-5 work days per week** with **2 commits per day**:

- Commit 1: implementation or refactor
- Commit 2: tests, docs, cleanup, sample config, or UI polish

That keeps your history natural and believable while still reaching the target volume.

## Success Criteria By August 31

- the repo has a clean README and screenshots
- a new user can install and run the tool locally
- there is a sample config and demo test project
- the CLI can run tests, retry failures, and generate reports
- the project history clearly shows planning, implementation, testing, and polish

## Getting Started

This repo starts as a scaffold plus roadmap. Development should follow the weekly plan in [docs/roadmap.md](docs/roadmap.md) and the commit suggestions in [docs/weekly-commit-plan.md](docs/weekly-commit-plan.md).

For early config design, see [docs/config-schema.md](docs/config-schema.md) and the starter sample in `testorbit.example.yml`.

## Early CLI Commands

- `testorbit version`
- `testorbit doctor --config testorbit.example.yml`
- `testorbit list --config testorbit.example.yml`
- `testorbit show unit --config testorbit.example.yml`
