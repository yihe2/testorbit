# Development Notes

## Early Decisions

- keep the first CLI implementation on the Python standard library
- prefer a working baseline over adding dependencies too early
- store examples and planning docs alongside code so the repo tells a clear story

## Near-Term Priorities

- keep config, runner, and history modules from leaking into each other
- start HTML report generation after the list/show flow feels solid
- keep tests passing after each small feature

## Guardrails

- avoid building a dashboard before the CLI is solid
- avoid multi-runner complexity until the pytest path feels good
- keep each week shippable and understandable from the commit history
