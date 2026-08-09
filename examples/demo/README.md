# Demo Shop

A tiny pytest project used to try TestOrbit without creating your own config.

```powershell
testorbit doctor
testorbit list
testorbit run unit --dry-run
```

Tasks:

- `unit` — `pytest tests`
- `smoke` — `pytest -m smoke`
- `api` — `pytest tests/api`

Run these commands from this directory so pytest can import `shop.py`. See [../../docs/quickstart.md](../../docs/quickstart.md).
