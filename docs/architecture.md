# Architecture Notes

TestOrbit is intentionally small, but the code should still keep a few clear boundaries.

## CLI Layer

`testorbit.cli` owns argument parsing, config lookup, user-facing messages, and exit codes.

## Runner Layer

`testorbit.runner` owns command execution and returns a structured result. Keeping this separate makes it easier to add timing, output capture, retries, and history storage without making the CLI command handlers too large.

Run results expose a small dictionary representation so future history and report features can reuse the same shape.

## Config Layer

Config loading currently lives in the CLI module while the schema is still small. If validation grows, it should move into a dedicated config module.

## Near-Term Direction

- capture command output when useful
- persist run metadata to local history
- keep subprocess behavior isolated behind runner tests
