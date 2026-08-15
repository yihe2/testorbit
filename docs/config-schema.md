# Config Schema Draft

This draft defines the initial shape of `testorbit.yml` for the MVP.

## Top-Level Structure

```yaml
tasks:
  unit:
    runner: pytest
    command: pytest tests
    tags:
      - fast
      - local
quarantine:
  - smoke
```

## Field Notes

- `tasks`: mapping of task name to task definition
- `runner`: optional hint for humans and docs, ignored at execution time
- `command`: required executable command string for the task
- `tags`: optional labels used later for filtering
- `quarantine`: optional list of task names that `run` should skip

## Validation Rules

- the root document must be a mapping
- `tasks` must be a mapping
- each task must define a `command`
- task names should be unique and CLI-friendly because `list`, `show`, and `run` look up the same keys
- `quarantine` must be a list of existing task names when present
- empty quarantine lists are treated the same as omitting the key

## Near-Term Extensions

These are out of the 1.0 cut if they are not already implemented:

- `default_args`
- `working_directory`
- `env`
- `retry_limit`
