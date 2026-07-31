# CI Integration

TestOrbit is meant to run the same way on a laptop and in GitHub Actions. Pass `--ci` so logs stay plain, and keep artifacts under `reports/`.

## Artifact Paths

CI jobs should write history into the reports directory so one upload captures everything:

```text
reports/runs.jsonl
reports/summary.html
reports/runs.json
```

Local runs still default to `run-history/runs.jsonl`. Override that in CI with `--history-path reports/runs.jsonl`.

## GitHub Actions

A copy-paste workflow lives at [examples/github-actions.yml](examples/github-actions.yml). Place it at `.github/workflows/testorbit.yml` in a project that already has `testorbit.yml`.

The important steps are:

```bash
testorbit --ci run unit --history-path reports/runs.jsonl
testorbit --ci export-history --history-path reports/runs.jsonl
testorbit --ci report --history-path reports/runs.jsonl
```

`export-history` and `report` use `if: always()` in the sample so a failing task still publishes JSON and HTML. Upload the `reports/` folder as a workflow artifact.

This repository's own checks live in `.github/workflows/ci.yml`. They install the package, run `pytest`, then render an HTML report from whatever history exists (empty history still writes a page).

## Local Parity

The same commands work outside GitHub Actions:

```powershell
testorbit --ci doctor --config testorbit.example.yml
testorbit --ci report --history-path reports/runs.jsonl
```

`--ci` turns off color and other interactive styling so captured logs match CI output.
