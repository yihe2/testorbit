# Weekly Commit Plan

This plan keeps the history realistic at **8-10 commits per week**. Aim for **2 commits per work day** across **4-5 days**.

## Commit Pattern

- Day A: feature scaffold + tests/docs
- Day B: feature implementation + validation/refactor
- Day C: UX polish + tests
- Day D: integration + docs
- Day E: optional buffer, bug fixes, cleanup

## Week-by-Week Commit Themes

### Week 1

1. initialize repository structure
2. add README with project vision
3. add roadmap and milestone plan
4. add pyproject and package skeleton
5. define config schema draft
6. add base unit test setup
7. document development workflow
8. refine project scope and backlog

### Week 2

1. add CLI app entrypoint
2. wire `--help` and version output
3. implement YAML config loader
4. add config validation errors
5. support named task parsing
6. add config tests
7. improve CLI messaging
8. clean package structure

### Week 3

1. add run command shell execution
2. return proper exit codes
3. capture stdout/stderr summary
4. add runner tests
5. improve command error handling
6. support task lookup by name
7. add example config file
8. refresh README usage section

### Week 4

1. add pytest adapter abstraction
2. implement pytest command builder
3. pass through extra CLI flags
4. capture duration metadata
5. persist run history JSON
6. add history tests
7. improve terminal rendering
8. document pytest workflow

### Week 5

1. add include filter support
2. add exclude filter support
3. support task tags
4. validate conflicting options
5. improve stored run metadata
6. expand parser tests
7. refine CLI examples
8. bug-fix and cleanup pass

### Week 6

1. add retry command
2. store failed test references
3. support configurable retry count
4. add retry orchestration tests
5. improve failure summaries
6. document retry workflow
7. refactor execution service
8. polish error output

### Week 7

1. add list command
2. add show command
3. display last run summary
4. improve command help text
5. add output formatting tests
6. refine service boundaries
7. document task discovery flow
8. cleanup naming inconsistencies

### Week 8

1. add JSON export command
2. define report data model
3. add HTML template scaffold
4. render initial summary page
5. add report rendering tests
6. improve artifact directory layout
7. document report usage
8. cleanup report code

### Week 9

1. finalize HTML summary cards
2. add pass/fail charts or table
3. link report path in CLI output
4. add sample generated artifact
5. improve report styling
6. add end-to-end report test
7. update README screenshots section
8. bug-fix report edge cases

### Week 10

1. add init command
2. generate starter config
3. add sample task presets
4. validate generated file contents
5. add init tests
6. improve first-run messaging
7. document quickstart flow
8. cleanup CLI options

### Week 11

1. improve missing-tool detection
2. harden Windows path handling
3. improve subprocess error mapping
4. add regression tests
5. refactor runner internals
6. improve logging output
7. document troubleshooting
8. cleanup technical debt

### Week 12

1. track repeated failures
2. mark flaky indicators in history
3. surface flaky hints in report
4. add history aggregation tests
5. document flaky concept
6. refine data model
7. polish summaries
8. bug-fix aggregation edge cases

### Week 13

1. add quarantine config block
2. skip quarantined tests
3. warn when quarantine is active
4. add quarantine tests
5. improve config documentation
6. add sample quarantine scenarios
7. refine report labels
8. cleanup config naming

### Week 14

1. add GitHub Actions workflow example
2. add CI output mode
3. standardize artifact paths
4. verify report generation in CI
5. document CI integration
6. add workflow badges
7. improve non-interactive output
8. cleanup CI docs

### Week 15

1. add demo project fixture
2. add sample tests for demo
3. refine quickstart example
4. capture README screenshots
5. improve onboarding text
6. add setup verification notes
7. test docs instructions
8. polish repository presentation

### Week 16

1. spike generic npm adapter
2. abstract adapter interface where needed
3. add adapter tests
4. evaluate keep-or-cut decision
5. improve docs if kept
6. remove complexity if not worth it
7. stabilize architecture
8. cleanup optional code paths

### Week 17

1. bug fix from real usage
2. improve edge-case coverage
3. tighten report rendering
4. simplify confusing CLI paths
5. polish config validation
6. improve exit-code behavior
7. cleanup TODOs
8. re-check install flow

### Week 18

1. prepare release checklist
2. finalize README badges and sections
3. refresh screenshots and examples
4. update changelog or release notes
5. cut version 1.0.0
6. final regression test pass
7. write project retrospective
8. archive post-release ideas

## Notes

- If one day produces a large feature, split the second commit into tests or docs.
- Avoid empty cosmetic commits that do not tell a story.
- Every week should leave the repo in a working state.
