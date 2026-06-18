# Reports

TestOrbit can turn local run history into a JSON export and a first HTML summary page.

Generated files default to the `reports/` directory, which is gitignored:

```text
reports/summary.html
reports/runs.json
```

## HTML Summary

```powershell
testorbit report --history-path tmp/runs.jsonl
testorbit report --history-path tmp/runs.jsonl --output tmp/summary.html
testorbit report --history-path tmp/runs.jsonl --status failed
```

The page shows pass/fail totals and one table row per recorded run. Empty history still writes a page with a "No run history found." row.

## JSON Export

```powershell
testorbit export-history --history-path tmp/runs.jsonl
testorbit export-history --history-path tmp/runs.jsonl --output reports/runs.json
```

Use `--output` when you want a path other than the default artifact location.
