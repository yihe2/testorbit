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
```

## Field Notes

- `tasks`: mapping of task name to task definition
- `runner`: optional hint for adapter selection
- `command`: executable command string for the task
- `tags`: optional labels used later for filtering

## Validation Rules

- the root document must be a mapping
- `tasks` must be a mapping
- each task must define a `command`
- task names should be unique and CLI-friendly

## Near-Term Extensions

- `default_args`
- `working_directory`
- `env`
- `retry_limit`
