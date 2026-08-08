# Quickstart

Install the package, then try the demo project before generating a config of your own.

```powershell
pip install -e ".[dev]"
cd examples/demo
testorbit doctor
testorbit list
testorbit show unit
testorbit run unit --dry-run
```

The demo ships a small shop module plus `unit`, `smoke`, and `api` tasks. `doctor` should report three tasks. `run unit --dry-run` should print `pytest tests` without starting pytest.

To execute a task for real, stay in `examples/demo` so pytest can see `shop.py`:

```powershell
testorbit run unit
testorbit run smoke
testorbit history
testorbit report
```

`run` writes `run-history/runs.jsonl`. `report` writes `reports/summary.html`. Both folders are gitignored.

## Starter Config In A New Project

From an empty project folder:

```powershell
testorbit init
testorbit doctor
testorbit list
testorbit show unit
testorbit run unit --dry-run
```

`init` writes `testorbit.yml` with the same `unit`, `smoke`, and `api` pytest presets the demo uses. It refuses to overwrite an existing file unless you pass `--force` or a different `--config` path.

`testorbit.example.yml` at the repo root is another read-only sample if you want to inspect the schema without changing directories.

After a clone, [setup.md](setup.md) is the checklist for Python, the editable install, package tests, and the demo CLI.
