# Run History

TestOrbit stores task run metadata as newline-delimited JSON.

By default, run records are written to:

```text
run-history/runs.jsonl
```

Each record includes:

- task name
- command
- exit code
- duration in seconds

Use `--history-path` to write history somewhere else:

```powershell
testorbit run unit --config testorbit.example.yml --history-path tmp/runs.jsonl
```

Dry runs do not write history because they do not execute a task.
