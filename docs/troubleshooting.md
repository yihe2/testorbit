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

Check that the task is nested under the top-level `tasks` mapping. Task names should be short and easy to type because they are used directly in `list`, `show`, and `run`.

## Report File Is Missing

`testorbit report` writes to `reports/summary.html` by default. That folder is gitignored, so the file will not show up in git status. Pass `--output` if you want a different path.

## Command Not Found

`testorbit run` checks that the first token of the task command exists before starting a subprocess. Install the tool, add it to PATH, or use an absolute quoted path on Windows:

```yaml
tasks:
  unit:
    command: '"C:\Python311\python.exe" -m pytest tests'
```

## Permission Denied

The executable was found, but the operating system refused to start it. Confirm the path points at a real program and that you have permission to run it.

## Task Is Skipped As Quarantined

`run` exits 0 without starting the command when the task name is in the top-level `quarantine` list. Remove the name from that list, or run a different task.

```yaml
quarantine:
  - smoke
```

`doctor`, `list`, and `show` also surface the same list so a leftover skip is easier to notice.
