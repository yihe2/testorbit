# Development Notes

## Early Decisions

- keep the first CLI implementation on the Python standard library
- prefer a working baseline over adding dependencies too early
- store examples and planning docs alongside code so the repo tells a clear story

## Priorities

- keep config, runner, history, and report modules from leaking into each other
- keep tests passing after each small feature
- treat [post-release.md](post-release.md) as optional follow-up, not 1.0 debt

## Guardrails

- avoid building a dashboard before the CLI is solid
- do not add a second adapter before a real JavaScript demo exists
- keep each week shippable and understandable from the commit history

1.0.0 closed on August 31, 2026. Follow-ups are in [post-release.md](post-release.md).
