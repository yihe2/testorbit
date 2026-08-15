# Adapter Spike

Week 16 tried a small command adapter so a task could omit `command` when `runner` was `pytest`, `npm`, or `jest`.

## What Worked

An explicit `command` still wins. `runner: npm` with no command becomes `npm test`. That is enough to prove a second runtime could be represented as a default string.

## Keep Or Cut

**Cut.** The project ships on August 31, 2026. The roadmap already says to drop secondary adapter support first if time is tight.

Reasons:

- `command: npm test` already runs npm through the generic shell runner. A named adapter does not add execution capability.
- this repo has no JavaScript demo, so `jest` / `npm` defaults would be untested in a real project.
- defaulting a missing command hides config mistakes. Requiring `command` is clearer for `doctor` and for newcomers.
- two weeks remain for bug-fix and release work. Extra adapter types would need docs, examples, and Windows PATH handling for `npm`.

## 1.0 Shape

Keep the shell runner. Treat `runner` as an optional hint in YAML, not as a command factory. Tasks must define `command`. The spike mapping was removed after this decision so the 1.0 path stays command-only.
