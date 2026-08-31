# Post-Release Ideas

These are intentionally out of 1.0. They are next-project work, not open 1.0 bugs.

## Retry Failed Tasks

`testorbit retry` (or `run --retry`) should re-execute the last failed task names from JSONL history, with a small cap so a broken suite cannot loop.

## Include And Exclude

`--include` / `--exclude` on `run` and `list`, matching task names or `tags`. Conflicting options should fail in `doctor` and at parse time.

## Duration Trends

A second report section that groups average duration by task name. Keep it in the HTML page; do not add a database.

## Terminal Themes

Optional color themes on top of Rich. `--ci` must still force plain output.

## JavaScript Demo

Only revisit a named npm adapter if this repo gains a real JS fixture. Until then, document `command: npm test` and stop.
