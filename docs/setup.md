# Setup Verification

Use this checklist after a fresh clone. None of these steps should require extra config files.

## 1. Python

```powershell
python --version
```

TestOrbit needs **Python 3.11 or newer**. The Windows `python` stub from the Store does not count; install a real interpreter and confirm it prints a version.

## 2. Editable Install

From the repository root:

```powershell
pip install -e ".[dev]"
testorbit version
```

Expect `TestOrbit 1.0.0`. If the command is not found, the scripts directory for that interpreter is not on PATH.

Confirm the install includes the HTML template:

```powershell
python -c "from testorbit.report import TEMPLATES_DIR, SUMMARY_TEMPLATE; print((TEMPLATES_DIR / SUMMARY_TEMPLATE).exists())"
```

That should print `True`. `pip show testorbit` should list the package location.

## 3. Package Tests

```powershell
pytest
```

This runs `tests/` for the CLI itself. It does not collect `examples/demo/tests`.

## 4. Demo CLI

```powershell
cd examples/demo
testorbit doctor
testorbit list
testorbit run unit --dry-run
```

Expect three discovered tasks and `Would run: pytest tests`. If `doctor` cannot find the config, you are not in `examples/demo`.

Running `testorbit run unit` (without `--dry-run`) needs pytest on PATH, which the `[dev]` extra provides.

## 5. Report Path

```powershell
testorbit report
```

A page should appear at `examples/demo/reports/summary.html`. That folder is gitignored, so a missing file in `git status` is expected.
