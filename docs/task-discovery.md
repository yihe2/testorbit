# Task Discovery

TestOrbit discovers work from a YAML config file instead of scanning the filesystem for tests.

## Lookup Order

1. Load the file passed with `--config`, or `testorbit.yml` in the current directory.
2. Read the top-level `tasks` mapping.
3. Treat each key as a CLI task name such as `unit`, `smoke`, or `api`.
4. Require every task to define a `command`.

`doctor`, `list`, `show`, and `run` all validate that shape. `list` prints the discovered names. `show` prints one task's fields.

## Commands That Use Discovery

```powershell
testorbit doctor --config testorbit.example.yml
testorbit list --config testorbit.example.yml
testorbit show unit --config testorbit.example.yml
```

If run history exists, `list` and `show` also attach the latest recorded status for each task. Missing history is not an error; those commands still work from the config file alone.

## Why Names Matter

Task names are the CLI API. Keep them short, unique, and easy to type because `run`, `show`, and later retry flows all look up the same keys.