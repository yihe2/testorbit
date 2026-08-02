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

- summary cards for total runs, passed, failed, and flaky tasks
- a pass/fail bar chart
- a table of recorded runs with a Result column
- a repeated-failure hint when a task has failed at least twice

The CLI prints the resolved report path and a `file://` link so the page can be opened from the terminal. `testorbit --ci report` prints the path only, which is easier to scan in GitHub Actions logs.

Empty history still writes a page with a "No recorded runs." row. Missing task names, statuses, or durations are filled in before rendering.

See [flaky.md](flaky.md) for how repeated failures are counted.

CI jobs should pass `--history-path reports/runs.jsonl` so the JSONL log lands next to `summary.html` and `runs.json`. See [ci.md](ci.md).

## JSON Export

```powershell
testorbit export-history --history-path tmp/runs.jsonl
testorbit export-history --history-path tmp/runs.jsonl --output reports/runs.json
```

Use `--output` when you want a path other than the default artifact location.
