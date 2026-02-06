# Feature: Task 1 — Spec-driven Implementation

## Summary
Scaffolded feature spec for Task 1. This spec follows the repository's Spec-First/TDD gates: includes acceptance criteria, failing-test placeholders, telemetry requirements (Tenx MCP Sense), and a minimal implementation plan.

## Context
- Owner: data-engineering / integrator
- Branch: task-1

## Goals
- Provide a precise, testable specification to drive TDD development for Task 1.
- Ensure CI gates require this spec and related failing tests and telemetry snippets before merging.

## Acceptance Criteria
- A failing unit/integration test exists and demonstrates the expected behavior (TDD).
- Core service endpoints (or CLI) implement the behavior described below and pass the tests.
- Tenx MCP Sense telemetry events emitted for key lifecycle events (start, success, failure).

## Minimal API / CLI
- API: POST /task1/run — accepts JSON with `input` and returns `result`.
- CLI: `task1 run --input '<json>'` — returns JSON result on stdout.

## Data model (minimum)
- TaskRequest: {"id": string, "payload": object}
- TaskResult: {"id": string, "status": "ok"|"error", "output": object}

## Telemetry (Tenx MCP Sense)
- Emit `task1.started` with `task_id` and `payload_size` at start.
- Emit `task1.completed` with `task_id` and `duration_ms` on success.
- Emit `task1.failed` with `task_id` and `error` on failure.

## Failing-tests placeholders
- tests/test_task1_initial.py::test_run_returns_expected_structure — asserts that POST /task1/run returns `TaskResult` with `status: ok` and `output` is an object.
- tests/test_telemetry_task1.py::test_telemetry_events_emitted — asserts that telemetry events for start/completion are recorded.

## Tasks
- TASK-1.1: Write failing tests (TDD) — file: `tests/test_task1_initial.py` (P1)
- TASK-1.2: Implement CLI/API harness to satisfy test (P2)
- TASK-1.3: Add telemetry instrumentation and ensure events emitted (P3)
- TASK-1.4: Update CI command stubs to gate on spec/tests/telemetry (P4)

## Risks & Notes
- External services should be mocked in unit tests; integration tests can use local Dockerized Postgres/Weaviate if available.
- Telemetry contract must be stable; keep event names and payload keys exact.

## Links
- Repository constitution: .specify/memory/constitution.md
- Templates: .specify/templates/spec-template.md

<!-- End of scaffolded spec.md -->