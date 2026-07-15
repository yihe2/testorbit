# Reports

TestOrbit can turn local run history into a JSON export and an HTML summary page.

Generated files default to the `reports/` directory, which is gitignored:

```text
reports/summary.html
reports/runs.json
```

A committed sample of the current page lives at [examples/summary.html](examples/summary.html).

## HTML Summary

```powershell
testorbit report --history-path tmp/runs.jsonl
testorbit report --history-path tmp/runs.jsonl --output tmp/summary.html
testorbit report --history-path tmp/runs.jsonl --status failed
```

The page includes:

- summary cards for total, passed, and failed runs
- a pass/fail bar chart
- a table of recorded runs
- a flaky-task hint when a task has failed at least twice

The CLI prints the resolved report path and a `file://` link so the page can be opened from the terminal.

Empty history still writes a page with a "No run history found." row. Missing task names, statuses, or durations are filled in before rendering.

See [flaky.md](flaky.md) for how repeated failures are counted.

## JSON Export

```powershell
testorbit export-history --history-path tmp/runs.jsonl
testorbit export-history --history-path tmp/runs.jsonl --output reports/runs.json
```

Use `--output` when you want a path other than the default artifact location.
