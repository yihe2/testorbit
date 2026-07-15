# Flaky Tasks

TestOrbit treats a task as flaky when it has failed at least twice in the stored run history.

That threshold is intentionally small for the MVP. It is a local hint, not a CI quarantine list. A task can still pass later; the label means it has failed repeatedly, not that every run fails.

## How It Is Counted

- passing runs do not increment the failure count
- missing `status` values fall back to `exit_code`
- tasks with fewer than two failures are left unlabeled

`testorbit report` prints a flaky hint when any task crosses the threshold. The HTML table also marks those task names.

## Example

If `unit` fails, passes, then fails again, it is marked flaky. If `smoke` fails once, it is not.
