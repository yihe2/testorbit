# Release Checklist

Use this list before tagging a TestOrbit release.

## Product

- [ ] `testorbit version` matches `pyproject.toml`
- [ ] `pip install -e ".[dev]"` and the HTML template import both succeed ([setup.md](setup.md))
- [ ] `pytest` is green
- [ ] `examples/demo` responds to `doctor`, `list`, and `run unit --dry-run`
- [ ] `testorbit report` writes `reports/summary.html` from empty or real history

## Docs

- [ ] README install, demo, and screenshot sections match the current CLI
- [ ] [CHANGELOG.md](../CHANGELOG.md) has an entry for this version
- [ ] sample report at [examples/summary.html](examples/summary.html) matches the live template
- [ ] GitHub Actions example still uses `--ci` and `reports/`

## Cut

- [ ] bump `project.version` and `testorbit.__version__` together
- [ ] commit the bump as `Release x.y.z` (or equivalent)
- [ ] tag the commit after it is pushed
