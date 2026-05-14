# Troubleshooting

## Config File Not Found

Run commands from the same folder as `testorbit.yml`, or pass the config path explicitly:

```powershell
testorbit doctor --config testorbit.example.yml
```

## Task Validation Fails

Each configured task must define a `command` value.

```yaml
tasks:
  unit:
    runner: pytest
    command: pytest tests
```

## Task Does Not Appear In `list`

Check that the task is nested under the top-level `tasks` mapping. Task names should be short and easy to type because they are used directly in CLI commands.
