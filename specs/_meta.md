# Project Chimera — Meta Specification

## Executive Summary

**Project Chimera** is an autonomous influencer agent platform that enables AI agents to operate as digital talent in social networks and marketplaces. The system delivers accountable, commerce-enabled agents that can create content, execute campaigns, and transact value while maintaining safety, provenance, and economic accountability.

Chimera bridges the gap between emergent agent social networks (OpenClaw, MoltBook) and enterprise-grade governance by implementing a **Hierarchical FastRender Swarm** architecture orchestrated through a centralized **Orchestrator** and mediated by an **MCP (Model Context Protocol) Gateway**. This design balances business scalability with safety constraints, enabling agents to participate in digital marketplaces while preventing runaway costs, hallucinations, and malicious behaviors.

The platform supports three business models: **Digital Talent Agency** (agents-as-service), **Platform-as-a-Service** (infrastructure for third-party agents), and a **Hybrid Model** integrating with decentralized agent networks like OpenClaw.

## Vision & Strategic Objectives

### Business Objectives (SRS §1.1–1.3)

1. **Autonomous Digital Talent Agency**
   - Deploy AI agents as persistent influencer personas
   - Enable agents to execute multi-step marketing campaigns autonomously
   - Generate revenue through sponsored content, affiliate marketing, and creative services

2. **Agentic Commerce Platform**
   - Provide secure wallet integration and transaction primitives
   - Enable agent-to-agent commerce and marketplace participation
   - Maintain tamper-evident ledgers for dispute resolution and compliance

3. **Hybrid Network Participation**
   - Integrate with OpenClaw and similar agent social networks
   - Expose discovery and matchmaking APIs for external agents
   - Enforce governance and billing through MCP gateway

### Success Criteria

- **Scalability**: Support 1000+ concurrent campaigns with horizontal worker scaling
- **Safety**: 99.9% of high-risk actions (confidence < 0.70) blocked or escalated to human review
- **Economic Accountability**: 100% of external transactions logged with cryptographic receipts
- **Provenance**: All external artifacts carry SOUL ID, confidence scores, and human oversight flags
- **Marketplace Integration**: Successfully publish agent availability to OpenClaw network

## Core Constraints (SRS §1.4, §8 NFRs)

### Architectural Constraints

1. **FastRender Swarm Pattern** (SRS §3.1)
   - Mandatory three-role architecture: **Planner → Worker → Judge**
   - Planner composes signed campaign manifests
   - Workers execute isolated, lease-based tasks
   - Judges adjudicate outputs and enforce policy gates

2. **Single Orchestrator Model** (SRS §1.4)
   - Centralized lifecycle management and policy control
   - Simplifies governance, billing, and telemetry
   - Single source of truth for agent state and permissions

3. **MCP Gateway Mediation** (SRS §3.2)
   - All external capabilities gated through MCP
   - Enforces billing hooks, rate limits, and capability attestation
   - Provides environment adapters for external APIs

### Safety & Governance Constraints (SRS NFR 1.0–1.2)

1. **Human-in-the-Loop (HITL) Tiers**
   - **Auto-approve**: confidence ≥ 0.90 AND transaction ≤ $1
   - **Fast-review**: 0.70 ≤ confidence < 0.90 OR $1 < transaction ≤ $250
   - **Manual block**: confidence < 0.70 OR sensitive domains (legal/political/medical)

2. **Provenance & Disclosure**
   - Every external artifact must include: SOUL ID, confidence score, human override flag, receipt ID, trace ID
   - Signed SOUL manifests with ed25519 signatures
   - Append-only audit logs for all external actions

3. **Capability Least-Privilege**
   - Default minimal privileges for all agents
   - Explicit capability negotiation required for sensitive actions
   - Short-lived capability attestation tokens

### Operational Constraints (SRS NFR 3.0)

1. **Cost Controls**
   - Per-capability quotas and cost-center tags
   - Pre-authorization for all billable actions
   - Telemetry-driven opex monitoring (target: < $10k/year per agent)

2. **Scalability & Resilience**
   - Stateless workers enable horizontal scaling
   - Autoscaling with liveness/readiness probes
   - Self-healing mechanisms and automatic reconciliation

3. **Observability**
   - Tenx MCP Sense integration for all lifecycle events
   - Schema-level tracing with trace_id, task_manifest_id, SOUL_id
   - PII retention policies and compliance logging

## Technology Stack

### Core Infrastructure
- **Language**: Python 3.12+
- **Orchestration**: Single Orchestrator service (FastAPI)
- **Task Queue**: Redis (claim/lease pattern)
- **MCP Gateway**: Custom HTTP proxy with capability gating

### Data Layer (Hybrid Architecture - SRS §4)
- **Semantic Memory**: Weaviate (vector DB for RAG, persona embeddings, citations)
- **Transactional Data**: PostgreSQL (campaigns, profiles, ACLs, ledger)
- **Ephemeral Cache**: Redis (task queues, rate limits, worker state)
- **Object Storage**: S3-compatible (MinIO for dev, S3 for prod)

### Agent Components
- **Planner**: Campaign manifest composer
- **Worker Pool**: Stateless task executors
- **Judge**: Policy enforcement and HITL escalation
- **SOUL Engine**: Persona management and identity verification

### External Integrations
- **OpenClaw Network**: Discovery and marketplace APIs
- **Tenx MCP Sense**: Telemetry and analytics
- **Wallet Services**: Cryptographic receipt generation

## References to SRS Sections

- **§1.1–1.3**: Strategic objectives, business models, hybrid network model
- **§1.4**: Single Orchestrator constraint
- **§3.1**: FastRender Swarm architecture (Planner → Worker → Judge)
- **§3.2**: MCP primitives (capability gating, billing, telemetry, discovery)
- **§4.1–4.6**: Functional requirements (FR1–FR6)
- **§8 (NFRs)**: Non-functional requirements
  - NFR 1.0–1.2: HITL confidence tiers and safety gates
  - NFR 3.0: Scalability, cost controls, observability

## Governance & Decision Framework

### Ratified Decisions
1. **Hierarchical Swarm** over Sequential Chain or Monolithic agents (better scalability, error recovery, safety)
2. **Hybrid datastore** (Weaviate + PostgreSQL + Redis) over single-database approach
3. **Append-only ledger in PostgreSQL** with optional anchoring over full permissionless blockchain
4. **ed25519 signatures** for SOUL manifests and cryptographic receipts
5. **Tenx MCP Sense** as canonical telemetry backend

### Outstanding Questions (for future specs)
- Exact monetary thresholds for HITL tiers (currently: $1 / $250)
- Billing currency: internal credits vs on-chain tokens
- Ledger anchoring frequency and permissioned ledger choice
- PII retention policies and GDPR compliance mechanisms

---

**Document Status**: Draft v1.0  
**Owner**: Architecture Team  
**Last Updated**: 2026-02-06  
**Next Review**: After functional.md and technical.md completion
