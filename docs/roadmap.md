# TestOrbit Roadmap

## Timeline

- Start: **May 1, 2026**
- End: **August 31, 2026**
- Working cadence: **4-5 days per week**
- Commit target: **8-10 commits per week**
- Total target: **150-170 commits**

## Phase 1: Foundation

### Week 1: May 1 - May 3

- create repo structure
- write README and scope
- choose CLI stack and dependencies
- define config schema draft
- add package metadata

### Week 2: May 4 - May 10

- build first CLI command skeleton
- add config loader
- support reading named tasks
- add basic validation
- write initial unit tests

### Week 3: May 11 - May 17

- implement `run` command
- execute saved shell commands
- print clear pass/fail summaries
- add exit codes
- add smoke tests

### Week 4: May 18 - May 24

- add `pytest` adapter
- support passing extra flags
- capture duration and status
- save JSON run records
- improve terminal formatting

## Phase 2: MVP

### Week 5: May 25 - May 31

- add named filters and tags
- allow include/exclude patterns
- store recent run metadata
- improve error messages
- expand tests for config parsing

### Week 6: June 1 - June 7

- add failed-test retry command
- keep failed-case references
- support rerun count
- test retry flow
- document retry examples

### Week 7: June 8 - June 14

- add `list` and `show` commands
- display configured test tasks
- show last run summary
- improve CLI help text
- clean internal service boundaries

### Week 8: June 15 - June 21

- generate JSON summary exports
- start HTML report generation
- create report template structure
- add sample output artifacts
- test report rendering

### Week 9: June 22 - June 28

- finish MVP HTML report
- show pass/fail counts and timing
- add report links in CLI output
- document end-to-end usage
- record screenshots for README later

## Phase 3: Productization

### Week 10: June 29 - July 5

- add project init command
- generate starter config file
- include sample `pytest` task presets
- validate generated files
- test first-run experience

### Week 11: July 6 - July 12

- improve logging and error handling
- handle missing tools gracefully
- improve Windows path support
- add regression tests
- refactor execution pipeline

### Week 12: July 13 - July 19

- add flaky-test annotations
- track repeated failures in history
- mark unstable tasks in reports
- document intended workflow
- test history aggregation

### Week 13: July 20 - July 26

- add quarantine list support
- skip known unstable tests by config
- show quarantine warnings
- test skip behavior
- polish config examples

### Week 14: July 27 - August 2

- add GitHub Actions sample workflow
- add CI-friendly output mode
- generate artifacts in predictable paths
- document CI setup
- verify local/CI parity

## Phase 4: Polish And Release

### Week 15: August 3 - August 9

- create demo project fixtures
- add realistic sample test tasks
- capture screenshots and examples
- tighten README structure
- improve onboarding docs

### Week 16: August 10 - August 16

- optional secondary adapter spike
- try generic `npm test` integration
- decide whether to keep or drop it
- improve abstractions only if needed
- avoid overscoping

### Week 17: August 17 - August 23

- full bug-fix week
- improve test coverage
- remove rough edges
- polish terminal output
- stabilize reports and config validation

### Week 18: August 24 - August 31

- final release prep
- cut `v1.0.0`
- finalize screenshots, badges, and usage examples
- clean open issues and TODOs
- write release notes and project retrospective

## Scope Guardrails

If you start falling behind, cut in this order:

1. secondary adapter support
2. flaky-test annotations
3. quarantine support
4. advanced trend reporting

Do not cut:

- core CLI run flow
- config loading
- retry flow
- run history
- HTML report
- tests
- documentation
