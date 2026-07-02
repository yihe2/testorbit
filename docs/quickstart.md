# Quickstart

Create a starter config, then inspect and dry-run a task.

```powershell
testorbit init
testorbit doctor
testorbit list
testorbit show unit
testorbit run unit --dry-run
```

`init` writes `testorbit.yml` with `unit`, `smoke`, and `api` pytest presets. It refuses to overwrite an existing file unless you pass a different `--config` path.

After a real run, inspect history and render the HTML report:

```powershell
testorbit run unit
testorbit history
testorbit report
```

Use `testorbit.example.yml` in this repo if you want to try the CLI before generating your own config.
