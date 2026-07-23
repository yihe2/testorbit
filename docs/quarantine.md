# Quarantine

Use a top-level `quarantine` list when a named task should stay in the config but should not run.

`testorbit run` skips those names with a warning and exit code 0. It does not start the command and does not write history. `testorbit doctor` prints the same list so a forgotten skip is visible.

Flaky labels in history are separate. Quarantine is an explicit config choice, not something derived from past failures.

## Skip One Unstable Suite

Keep `smoke` defined, but stop executing it until the suite is stable again:

```yaml
tasks:
  unit:
    command: pytest tests
  smoke:
    command: pytest -m smoke
quarantine:
  - smoke
```

`testorbit run unit` still executes. `testorbit run smoke` prints `Skipping quarantined task 'smoke'`.

## Skip Local Integration Work

Park slower tasks that should not run on a laptop, then remove them from the list before CI:

```yaml
tasks:
  unit:
    command: pytest tests
  api:
    command: pytest tests/api
quarantine:
  - api
```

## Empty List

An empty list is valid and means nothing is skipped:

```yaml
tasks:
  unit:
    command: pytest tests
quarantine: []
```

Omitting `quarantine` has the same effect. Unknown names are rejected so a typo cannot silently skip nothing.
