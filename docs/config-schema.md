# Config Schema

`testorbit.yml` is a mapping of named tasks plus an optional quarantine list.

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
- task names must be non-empty CLI tokens with no whitespace
- `quarantine` must be a list of existing task names when present
- empty quarantine lists are treated the same as omitting the key
- duplicate quarantine names are ignored
- `tags`, when present, must be a list of non-empty strings

## Near-Term Extensions

These are out of the 1.0 cut if they are not already implemented:

- `default_args`
- `working_directory`
- `env`
- `retry_limit`
