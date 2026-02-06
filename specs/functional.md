# Project Chimera — Functional Requirements

## Overview

This document defines the functional requirements for Project Chimera using user-story format. Each requirement maps to SRS sections 4.1–4.6 and includes acceptance criteria.

**Format**: As a [role], I need [feature] so that [benefit].

---

## FR1 — Persona System (SRS §4.1)

### FR1.1: SOUL Manifest Creation

**As a** campaign manager,  
**I need** to create persistent agent personas with signed SOUL manifests,  
**So that** agents have verifiable identities for marketplace participation and provenance tracking.

**Acceptance Criteria**:
- SOUL manifest includes: agent_id, persona_name, schema_version, creation_timestamp, ed25519_signature
- Manifests are versioned and immutable once signed
- Signature verification succeeds for all published manifests
- SOUL IDs are globally unique and collision-resistant

**SRS Reference**: §4.1 Persona, FR1

---

### FR1.2: Persona Profile Management

**As a** content creator,  
**I need** to define agent personality traits, voice guidelines, and ethical boundaries,  
**So that** agents produce on-brand content aligned with campaign objectives.

**Acceptance Criteria**:
- Persona profiles include: voice_tone, content_themes, prohibited_topics, target_audience
- Profiles are stored in Weaviate as embeddings for RAG retrieval
- Agents can query their own persona context during task execution
- Profile updates trigger re-embedding and version increment

**SRS Reference**: §4.1 Persona, FR1

---

## FR2 — Perception & RAG (SRS §4.2)

### FR2.1: Retrieval-Augmented Generation

**As an** agent worker,  
**I need** to ground my responses with citations from semantic memory,  
**So that** I reduce hallucinations and provide traceable evidence for my outputs.

**Acceptance Criteria**:
- Workers query Weaviate for relevant context before generating content
- All generated content includes citation metadata (source_id, confidence, retrieval_timestamp)
- RAG queries return top-k results with similarity scores ≥ 0.75
- Citations are persisted in the ledger for audit trails

**SRS Reference**: §4.2 Perception, FR2

---

### FR2.2: Campaign Context Enrichment

**As a** planner agent,  
**I need** to enrich campaign manifests with historical performance data and market trends,  
**So that** workers can optimize content for engagement and conversion.

**Acceptance Criteria**:
- Campaign manifests include context embeddings from previous campaigns
- Workers retrieve similar campaigns and their KPIs during task planning
- Context includes: engagement_metrics, audience_demographics, successful_content_patterns
- Enrichment happens automatically during manifest composition

**SRS Reference**: §4.2 Perception, FR2

---

## FR3 — Creative Engine (SRS §4.3)

### FR3.1: AI-Generated Campaign Content

**As a** marketing agent,  
**I need** to generate social media posts, images, and videos aligned with campaign goals,  
**So that** I can execute multi-channel campaigns autonomously.

**Acceptance Criteria**:
- Workers generate text content using LLM with persona context injection
- Image generation integrates with DALL-E or Stable Diffusion APIs via MCP
- All generated assets include provenance metadata (generator_model, prompt_hash, confidence)
- Content passes Judge review before external publication

**SRS Reference**: §4.3 Creative Engine, FR3

---

### FR3.2: Content Quality Assurance

**As a** judge agent,  
**I need** to validate generated content against brand guidelines and safety policies,  
**So that** only high-quality, compliant content reaches external audiences.

**Acceptance Criteria**:
- Judge evaluates content for: brand_alignment, toxicity, factual_accuracy, legal_compliance
- Content with confidence < 0.70 is automatically blocked
- Content with 0.70 ≤ confidence < 0.90 is sent to human review queue
- Approved content receives cryptographic approval signature

**SRS Reference**: §4.3 Creative Engine, FR3, NFR 1.0–1.2

---

## FR4 — Action System (SRS §4.4)

### FR4.1: Multi-Step Workflow Execution

**As an** orchestrator,  
**I need** agents to execute complex, multi-step workflows with error recovery,  
**So that** campaigns can run autonomously without manual intervention.

**Acceptance Criteria**:
- Planner decomposes campaigns into atomic tasks with dependencies
- Workers claim tasks from Redis queue using lease-based locking
- Failed tasks are automatically retried (max 3 attempts) or escalated to Judge
- Workflow state is persisted in PostgreSQL for resumability

**SRS Reference**: §4.4 Action System, FR4, §3.1 FastRender Swarm

---

### FR4.2: External API Integration

**As a** worker agent,  
**I need** to interact with external APIs (social media, payment gateways, analytics),  
**So that** I can publish content, process transactions, and collect performance data.

**Acceptance Criteria**:
- All external API calls are mediated through MCP gateway
- Workers receive short-lived capability tokens for specific API endpoints
- API calls include billing metadata and are logged to telemetry
- Rate limits and quotas are enforced at the MCP layer

**SRS Reference**: §4.4 Action System, FR4, §3.2 MCP Primitives

---

## FR5 — Commerce (SRS §4.5)

### FR5.1: Secure Wallet Integration

**As a** marketplace participant,  
**I need** agents to have secure wallets for receiving payments and paying for services,  
**So that** agents can transact value autonomously within budget constraints.

**Acceptance Criteria**:
- Each agent has a dedicated wallet with balance tracking in PostgreSQL
- Wallet operations (debit, credit) are atomic and logged to append-only ledger
- All transactions generate cryptographic receipts (tx_id, amount, timestamp, signature)
- Pre-authorization checks prevent transactions exceeding agent budget

**SRS Reference**: §4.5 Commerce, FR5

---

### FR5.2: Transaction Ledger & Receipts

**As a** compliance officer,  
**I need** tamper-evident transaction records with cryptographic receipts,  
**So that** I can audit agent spending and resolve disputes.

**Acceptance Criteria**:
- Ledger uses append-only table with immutable write pattern
- Each transaction includes: tx_id, from_agent, to_agent, amount, purpose, receipt_hash
- Receipts are signed with ed25519 and stored in S3-compatible object store
- Optional periodic anchoring to permissioned ledger for tamper resistance

**SRS Reference**: §4.5 Commerce, FR5

---

### FR5.3: Billing & Cost Attribution

**As a** financial controller,  
**I need** to track per-agent and per-campaign costs with granular attribution,  
**So that** I can optimize spending and enforce budget limits.

**Acceptance Criteria**:
- All billable actions (API calls, LLM inference, storage) are tagged with cost_center_id
- MCP gateway enforces pre-authorization for actions exceeding cost thresholds
- Cost reports aggregate by agent, campaign, and capability type
- Budget alerts trigger when agents reach 80% of allocated budget

**SRS Reference**: §4.5 Commerce, FR5, NFR 3.0

---

## FR6 — Orchestration (SRS §4.6)

### FR6.1: Centralized Lifecycle Management

**As a** system operator,  
**I need** a single orchestrator to manage agent creation, activation, suspension, and termination,  
**So that** I have centralized control over the agent fleet.

**Acceptance Criteria**:
- Orchestrator exposes REST API for agent CRUD operations
- Agent states: CREATED, ACTIVE, SUSPENDED, TERMINATED
- State transitions are logged to audit trail with operator_id and reason
- Suspended agents cannot claim new tasks but can complete in-flight tasks

**SRS Reference**: §4.6 Orchestration, FR6, §1.4 Single Orchestrator

---

### FR6.2: Task Queue Management

**As a** planner agent,  
**I need** to enqueue tasks with priorities and dependencies,  
**So that** workers execute tasks in optimal order.

**Acceptance Criteria**:
- Tasks are stored in Redis with priority levels (HIGH, NORMAL, LOW)
- Workers claim tasks using FIFO within priority tiers
- Lease-based locking prevents duplicate execution (lease TTL: 5 minutes)
- Expired leases trigger automatic task re-queue

**SRS Reference**: §4.6 Orchestration, FR6, §3.1 FastRender Swarm

---

### FR6.3: Telemetry & Observability

**As a** DevOps engineer,  
**I need** comprehensive telemetry for all agent lifecycle events,  
**So that** I can monitor system health and debug failures.

**Acceptance Criteria**:
- All events emit to Tenx MCP Sense with schema: trace_id, task_manifest_id, SOUL_id, event_type, timestamp
- Event types include: agent.created, task.claimed, task.completed, task.failed, judge.approved, judge.escalated
- Telemetry includes performance metrics: task_duration_ms, queue_wait_time_ms, api_call_latency_ms
- PII is redacted from telemetry according to retention policy

**SRS Reference**: §4.6 Orchestration, FR6, NFR 3.0, Tenx MCP Sense

---

## Cross-Cutting Concerns

### Human-in-the-Loop (HITL)

**Applies to**: FR3 (Creative), FR4 (Actions), FR5 (Commerce)

**Confidence Tiers** (SRS NFR 1.0–1.2):
- **Auto-approve**: confidence ≥ 0.90 AND transaction ≤ $1
- **Fast-review**: 0.70 ≤ confidence < 0.90 OR $1 < transaction ≤ $250 (15-60 min SLA)
- **Manual block**: confidence < 0.70 OR sensitive domains (legal/political/medical)

### Provenance & Disclosure

**Applies to**: All external artifacts (FR3, FR4, FR5)

**Required Metadata**:
- SOUL_id: Agent identity
- confidence: Model confidence score (0.0–1.0)
- human_override_flag: Boolean indicating human review
- receipt_id: Transaction receipt reference
- trace_id: Telemetry trace identifier

---

**Document Status**: Draft v1.0  
**Owner**: Product Team  
**Last Updated**: 2026-02-06  
**Next Review**: After technical.md completion
