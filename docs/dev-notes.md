# Development Notes

## Early Decisions

- keep the first CLI implementation on the Python standard library
- prefer a working baseline over adding dependencies too early
- store examples and planning docs alongside code so the repo tells a clear story

## Near-Term Priorities

- keep config, runner, history, and report modules from leaking into each other
- bug-fix and release work through August 31
- keep tests passing after each small feature

## Guardrails

- avoid building a dashboard before the CLI is solid
- do not add a second adapter before 1.0; `command` already runs npm
- keep each week shippable and understandable from the commit history
