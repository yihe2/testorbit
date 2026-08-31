# Retrospective

TestOrbit started on May 1, 2026 as a four-month CLI portfolio and closed on August 31, 2026 at **1.0.0**.

The useful shape that survived is small: YAML tasks, a shell runner, JSONL history, and an HTML summary. Quarantine, flaky hints, `--ci`, and the demo shop were worth keeping. A second adapter was not. `command: npm test` already covers JavaScript suites, and Week 16 cut the extra mapping so the last two weeks could be bug-fix and release work.

## What Worked

- one command string per task, instead of a plugin system
- shipping `doctor` / `list` / `run` before reporting
- treating GitHub Actions as the same CLI with `--ci`, not a second product
- a demo project that newcomers can run without writing config

## What Slipped

The original must-ship list included include/exclude filters and a failed-test retry flow. Those never landed. History and reports ate the middle of the calendar, and by Week 16 the honest move was to finish 1.0 without them.

Retry and filters are recorded in [post-release.md](post-release.md), not as unfinished 1.0 work.

## Would Repeat

Keep the weekly cadence of four days and two real commits. Empty polish weeks would have been easier and less useful. The keep-or-cut adapter week is the one to copy on the next tool.
