# [PROJECT_NAME] Constitution
<!-- Example: Spec Constitution, TaskFlow Constitution, etc. -->

## Core Principles

### [PRINCIPLE_1_NAME]
<!-- Example: I. Library-First -->
[PRINCIPLE_1_DESCRIPTION]
<!-- Example: Every feature starts as a standalone library; Libraries must be self-contained, independently testable, documented; Clear purpose required - no organizational-only libraries -->

### [PRINCIPLE_2_NAME]
<!-- Example: II. CLI Interface -->
[PRINCIPLE_2_DESCRIPTION]
<!-- Example: Every library exposes functionality via CLI; Text in/out protocol: stdin/args → stdout, errors → stderr; Support JSON + human-readable formats -->

### [PRINCIPLE_3_NAME]
<!-- Example: III. Test-First (NON-NEGOTIABLE) -->
[PRINCIPLE_3_DESCRIPTION]
<!-- Example: TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced -->

### [PRINCIPLE_4_NAME]
<!-- Example: IV. Integration Testing -->
[PRINCIPLE_4_DESCRIPTION]
<!-- Example: Focus areas requiring integration tests: New library contract tests, Contract changes, Inter-service communication, Shared schemas -->

### [PRINCIPLE_5_NAME]
<!-- Example: V. Observability, VI. Versioning & Breaking Changes, VII. Simplicity -->
[PRINCIPLE_5_DESCRIPTION]
<!-- Example: Text I/O ensures debuggability; Structured logging required; Or: MAJOR.MINOR.BUILD format; Or: Start simple, YAGNI principles -->

## [SECTION_2_NAME]
<!-- Example: Additional Constraints, Security Requirements, Performance Standards, etc. -->

[SECTION_2_CONTENT]
<!-- Example: Technology stack requirements, compliance standards, deployment policies, etc. -->

## [SECTION_3_NAME]
<!-- Example: Development Workflow, Review Process, Quality Gates, etc. -->

[SECTION_3_CONTENT]
<!-- Example: Code review requirements, testing gates, deployment approval process, etc. -->

## Governance
<!-- Example: Constitution supersedes all other practices; Amendments require documentation, approval, migration plan -->

```markdown
# Autonomous AI Influencer — Infrastructure & Governance Constitution
<!--
Sync Impact Report
- Version change: none -> 0.1.0
- Modified/Added Principles: Spec-First Development; Test-First TDD; Agent Skill Contracts; Observability & Telemetry; Safety & Governance; Reproducible Build & Containerization; Versioning & Change Management
- Added Sections: Security, Safety & Compliance; Development Workflow & Quality Gates
- Removed Sections: none
- Templates reviewed:
	- .specify/templates/plan-template.md (checked / aligns with Constitution gates) ✅
	- .specify/templates/spec-template.md (checked / aligns) ✅
	- .specify/templates/tasks-template.md (reviewed; action items to enforce constitution gates) ⚠ pending
	- .specify/templates/agent-file-template.md (review required) ⚠ pending
	- .specify/templates/checklist-template.md (review required) ⚠ pending
- Commands folder: .specify/templates/commands/ not present — create command stubs to enforce gates ⚠ pending
- Follow-up TODOs:
	- TODO(RATIFICATION_DATE): confirm and record original adoption date
	- Update tasks/spec templates to include explicit constitution gate checks (TBD)
	- Add CI policy snippets to templates to run Tenx MCP Sense telemetry checks
Last amended: 2026-02-06
-->

## Core Principles

### 1. Spec-First Development (NON-NEGOTIABLE)
All work begins with a formal specification in the GitHub Spec Kit format. Specs must declare scope, inputs, outputs, user stories, acceptance tests and a measurable success criterion before any implementation begins. Specifications are the single source of truth for agent behavior and must be reviewed and accepted by the product owner prior to PRs that implement functionality.

### 2. Test-First (TDD) and Failing Tests as Design
Tests (unit, contract, and integration) are written to capture expected behavior before code is implemented. Tests MUST fail initially; passing tests only occur after implementation and verification. TDD enforces precise behavior, enables safe refactors, and serves as executable documentation for agents.

### 3. Agent Skill Contracts (Strict I/O Contracts)
Every agent capability (skill) MUST be defined with an explicit input/output contract: data schema, allowed side-effects, rate limits, and error semantics. Contracts are machine- and human-readable, included with the spec, and validated by contract tests. Changes to a contract require a versioned migration plan and automated compatibility checks.

### 4. Observability & Telemetry (Traceability required)
All runtime components must emit structured telemetry and traces compatible with Tenx MCP Sense. Logs, traces, and metrics MUST include correlation IDs, timestamps in ISO8601, and minimal PII policy adherence. Observability artifacts are first-class deliverables and required in PRs that change runtime behavior.

### 5. Safety, Privacy & Governance Constraints
Every spec must include explicit safety constraints (content filters, rate limits, human approval gates where required), data retention rules, and privacy handling. Autonomous behaviors that affect external systems require an explicit human-in-the-loop approval step captured in the spec and enforced by CI checks.

### 6. Reproducible Builds & Containerization
Deliverables MUST include deterministic container builds (Docker + pinned dependencies) and a Makefile for common tasks (build, test, lint, local-run). Builds must be reproducible and produce artifacts suitable for CI/CD and air-gapped environments.

### 7. Semantic Versioning & Change Management
All specs, APIs, and agent skill contracts follow semantic versioning. Backward-incompatible changes require MAJOR version bumps, a migration plan, and a deprecation window. Minor/patch changes must be documented and validated via automated compatibility checks in CI.
```markdown
# Autonomous AI Influencer — Infrastructure & Governance Constitution
<!--
Sync Impact Report
- Version change: none -> 0.1.0
- Modified/Added Principles: Spec-First Development; Test-First TDD; Agent Skill Contracts; Observability & Telemetry; Safety & Governance; Reproducible Build & Containerization; Versioning & Change Management
- Added Sections: Security, Safety & Compliance; Development Workflow & Quality Gates
- Removed Sections: none
- Templates reviewed:
  - .specify/templates/plan-template.md (checked / aligns with Constitution gates) ✅
  - .specify/templates/spec-template.md (checked / aligns) ✅
  - .specify/templates/tasks-template.md (reviewed; action items to enforce constitution gates) ⚠ pending
  - .specify/templates/agent-file-template.md (review required) ⚠ pending
  - .specify/templates/checklist-template.md (review required) ⚠ pending
- Commands folder: .specify/templates/commands/ not present — create command stubs to enforce gates ⚠ pending
- Follow-up TODOs:
  - TODO(RATIFICATION_DATE): confirm and record original adoption date
  - Update tasks/spec templates to include explicit constitution gate checks (TBD)
  - Add CI policy snippets to templates to run Tenx MCP Sense telemetry checks
Last amended: 2026-02-06
-->

## Core Principles

### 1. Spec-First Development (NON-NEGOTIABLE)
All work begins with a formal specification in the GitHub Spec Kit format. Specs must declare scope, inputs, outputs, user stories, acceptance tests and a measurable success criterion before any implementation begins. Specifications are the single source of truth for agent behavior and must be reviewed and accepted by the product owner prior to PRs that implement functionality.

### 2. Test-First (TDD) and Failing Tests as Design
Tests (unit, contract, and integration) are written to capture expected behavior before code is implemented. Tests MUST fail initially; passing tests only occur after implementation and verification. TDD enforces precise behavior, enables safe refactors, and serves as executable documentation for agents.

### 3. Agent Skill Contracts (Strict I/O Contracts)
Every agent capability (skill) MUST be defined with an explicit input/output contract: data schema, allowed side-effects, rate limits, and error semantics. Contracts are machine- and human-readable, included with the spec, and validated by contract tests. Changes to a contract require a versioned migration plan and automated compatibility checks.

### 4. Observability & Telemetry (Traceability required)
All runtime components must emit structured telemetry and traces compatible with Tenx MCP Sense. Logs, traces, and metrics MUST include correlation IDs, timestamps in ISO8601, and minimal PII policy adherence. Observability artifacts are first-class deliverables and required in PRs that change runtime behavior.

### 5. Safety, Privacy & Governance Constraints
Every spec must include explicit safety constraints (content filters, rate limits, human approval gates where required), data retention rules, and privacy handling. Autonomous behaviors that affect external systems require an explicit human-in-the-loop approval step captured in the spec and enforced by CI checks.

### 6. Reproducible Builds & Containerization
Deliverables MUST include deterministic container builds (Docker + pinned dependencies) and a Makefile for common tasks (build, test, lint, local-run). Builds must be reproducible and produce artifacts suitable for CI/CD and air-gapped environments.

### 7. Semantic Versioning & Change Management
All specs, APIs, and agent skill contracts follow semantic versioning. Backward-incompatible changes require MAJOR version bumps, a migration plan, and a deprecation window. Minor/patch changes must be documented and validated via automated compatibility checks in CI.
<!--
Sync Impact Report
- Version change: none -> 0.1.0
- Modified/Added Principles: Spec-First Development; Test-First TDD; Agent Skill Contracts; Observability & Telemetry; Safety & Governance; Reproducible Build & Containerization; Versioning & Change Management
- Added Sections: Security, Safety & Compliance; Development Workflow & Quality Gates
- Removed Sections: none
- Templates reviewed:
	- .specify/templates/plan-template.md (checked / aligns with Constitution gates) ✅
	- .specify/templates/spec-template.md (checked / aligns) ✅
	- .specify/templates/tasks-template.md (reviewed; action items to enforce constitution gates) ⚠ pending
	- .specify/templates/agent-file-template.md (review required) ⚠ pending
	- .specify/templates/checklist-template.md (review required) ⚠ pending
- Commands folder: .specify/templates/commands/ not present — create command stubs to enforce gates ⚠ pending
- Follow-up TODOs:
	- TODO(RATIFICATION_DATE): confirm and record original adoption date
	- Update tasks/spec templates to include explicit constitution gate checks (TBD)
	- Add CI policy snippets to templates to run Tenx MCP Sense telemetry checks
Last amended: 2026-02-06
-->

# Autonomous AI Influencer — Infrastructure & Governance Constitution

## Core Principles

### 1. Spec-First Development (NON-NEGOTIABLE)
All work begins with a formal specification in the GitHub Spec Kit format. Specs must declare scope, inputs, outputs, user stories, acceptance tests and a measurable success criterion before any implementation begins. Specifications are the single source of truth for agent behavior and must be reviewed and accepted by the product owner prior to PRs that implement functionality.

### 2. Test-First (TDD) and Failing Tests as Design
Tests (unit, contract, and integration) are written to capture expected behavior before code is implemented. Tests MUST fail initially; passing tests only occur after implementation and verification. TDD enforces precise behavior, enables safe refactors, and serves as executable documentation for agents.

### 3. Agent Skill Contracts (Strict I/O Contracts)
Every agent capability (skill) MUST be defined with an explicit input/output contract: data schema, allowed side-effects, rate limits, and error semantics. Contracts are machine- and human-readable, included with the spec, and validated by contract tests. Changes to a contract require a versioned migration plan and automated compatibility checks.

### 4. Observability & Telemetry (Traceability required)
All runtime components must emit structured telemetry and traces compatible with Tenx MCP Sense. Logs, traces, and metrics MUST include correlation IDs, timestamps in ISO8601, and minimal PII policy adherence. Observability artifacts are first-class deliverables and required in PRs that change runtime behavior.

### 5. Safety, Privacy & Governance Constraints
Every spec must include explicit safety constraints (content filters, rate limits, human approval gates where required), data retention rules, and privacy handling. Autonomous behaviors that affect external systems require an explicit human-in-the-loop approval step captured in the spec and enforced by CI checks.

### 6. Reproducible Builds & Containerization
Deliverables MUST include deterministic container builds (Docker + pinned dependencies) and a Makefile for common tasks (build, test, lint, local-run). Builds must be reproducible and produce artifacts suitable for CI/CD and air-gapped environments.

### 7. Semantic Versioning & Change Management
All specs, APIs, and agent skill contracts follow semantic versioning. Backward-incompatible changes require MAJOR version bumps, a migration plan, and a deprecation window. Minor/patch changes must be documented and validated via automated compatibility checks in CI.

## Security, Safety & Compliance
Security, privacy, and content-safety are integral to the design and cannot be deferred. Each spec MUST state:
- Data classification and retention policy for every data element
- Required content safety filters and acceptable-content policy
- Required access controls and secret management approach
- Audit and traceability expectations (who approved what, when)

Compliance checks (linting, static analysis, content-safety checks) are part of CI and are gating: failing these checks blocks merges.

## Development Workflow & Quality Gates
Work flows through these stages: Spec → Tests (failing) → Implementation → CI (automatic checks; telemetry enforcement) → Review → Staging → Production. Mandatory gates:
- Spec acceptance by product owner
- All tests pass in CI (unit, contract, integration)
- Telemetry/trace samples provided for runtime-affecting changes
- Risk review for any autonomous action that performs external effects

Pull requests must include links to spec, failing test artifacts, and a short migration plan for changes that affect contracts or behavior.

## Governance
This constitution is the authoritative governance layer for repository practices. Key rules:
- Amendments: Proposals are made via a dedicated spec PR titled "Constitution Amendment", include rationale, migration plan, and tests. Amendments require approval from at least two maintainers and one product representative.
- Enforcement: CI includes automated constitution checks (spec presence, failing tests, telemetry snippets). Any PR that violates a constitution gate is blocked until compliant.
- Versioning policy: Use MAJOR.MINOR.PATCH semantic versioning for the constitution and require a migration narrative for MAJOR bumps.
- Compliance review cadence: Quarterly governance reviews with an audit of tenancy, telemetry coverage, and safety gates.

**Version**: 0.1.0 | **Ratified**: TODO(RATIFICATION_DATE): confirm adoption date | **Last Amended**: 2026-02-06
