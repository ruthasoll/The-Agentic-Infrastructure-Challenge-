# tasks.md — Task 1 Implementation

## Phases & Tasks

- Setup
  - T1.1: Create virtualenv, update `pyproject.toml` if needed. (sequential)
  - T1.2: Ensure linting and formatting tools configured. (sequential)

- Tests
  - T2.1 [P]: Write `tests/test_task1_initial.py::test_run_returns_expected_structure` (failing)
  - T2.2 [P]: Write `tests/test_telemetry_task1.py::test_telemetry_events_emitted` (failing)

- Core
  - T3.1: Implement `task1` package worker function to satisfy T2.1
  - T3.2: Add CLI shim `task1/cli.py` and HTTP test server `task1/server.py`

- Integration
  - T4.1: Add DB mocks and integration test harness
  - T4.2: Validate telemetry sink integration (local file or test spy)

- Polish
  - T5.1: Add mermaid diagrams and JSON schemas
  - T5.2: Wire CI checks to `.github/workflows` (spec/tests/telemetry gates)

## Notes
- Parallel marker [P] indicates tasks that can be developed in parallel (tests can be authored by multiple engineers).
- Tests must fail first (TDD) before implementation tasks T3.* run.

<!-- End tasks.md -->