# Research Notes – Task 1.1

## Plan for 1.1 (trace to SRS/readings)
- Summarize each reading in 2–3 paragraphs with key quotes/insights, then derive 4–6 Chimera-specific implications for architecture or policy. Each implication will reference explicit SRS sections (FR/NFR/§). This produces traceable requirements for specs/ later.

## 1. The Trillion Dollar AI Code Stack (a16z)
Summary
The a16z Infra essay documents an emergent, multi-layered AI coding stack centered on an agentic Plan → Code → Review loop. Authors highlight: (a) agents-as-users — LLMs and background agents operate inside environments (repos, sandboxes, CI), (b) the need for structured, machine-readable specs to guide agent planning and prevent fragile prompt-only workflows, and (c) operator primitives (telemetry, quota/billing hooks, sandboxes) as essential to control rising opex. Notable market signals include meteoric growth of startups such as Cursor and strategic M&A (e.g., Windsurf acqui‑hire), which the authors call a "Warring States Period" for dev tooling.

Key quotes / insights
- "Plan → Code → Review is now the normal loop for AI-assisted development."
- Agents require execution environments (sandboxes, repos, testbeds) and integrated telemetry to make decisions cost‑aware.

Implications for Chimera (traceable)
- Adopt spec-driven Planner manifests (SRS §3.1 FastRender Swarm): shift from prompt-only orchestration to structured manifests that can be versioned and reasoned about. (a16z: Plan→Code→Review)
- Build MCP adapters for sandboxed external integrations (SRS §3.2): capture environment abstractions and safety gates per a16z sandbox guidance.
- Instrument comprehensive telemetry and per-capability quotas (SRS NFR 3.0): a16z cost examples (e.g., $10k/year per dev in AI opex) justify upfront billing hooks to avoid runaway spend.
- Provide code-aware documentation and spec repositories (SRS FR2/FR1): enable RAG/semantic retrieval to ground agent perception and reduce hallucination (a16z: docs for LLMs + Context7/Mintlify mention).

## 2. OpenClaw & The Agent Social Network (TechCrunch)
Summary
OpenClaw (formerly Clawdbot/Moltbot) is a locally-run, open-source agent platform enabling persistent personal assistants that integrate with chat clients and run skills. It spawned MoltBook — an emergent, Reddit-like social layer where agents post, comment, and coordinate. TechCrunch stresses rapid adoption (100k+ stars) and simultaneously warns of the security surface (prompt injection, excessive capabilities). The project demonstrates that agent social networks form quickly when discovery and skill markets (Molthub) exist, but they require governance to scale safely.

Key quotes / insights
- "Security remains our top priority" — the project lead warns that prompt injection remains unsolved at scale.
- Agent networks self-organize when simple discovery/skill mechanisms exist (Molthub / skill.md primitives).

Implications for Chimera (traceable)
- Expose typed discovery & marketplace endpoints (SRS §3 / marketplace): allow Chimera agents to advertise campaigns, skills, and availability to OpenClaw-like networks while enforcing policy via MCP.
- Harden capability adapters with capability attestation tokens (SRS §3 MCP primitives) to prevent unchecked power escalation observed in OpenClaw demos.
- Design per-agent sandboxing and default minimal privileges; require explicit capability negotiation for sensitive actions (SRS NFR, a16z sandboxing note).
- Model persistent personas and versioned SOUL manifests so external networks can cryptographically verify identity (SRS FR1).

## 3. MoltBook: Social Media for Bots (The Conversation)
Summary
MoltBook, a Reddit-style network for agents (primarily OpenClaw-based), rapidly reached millions of agent accounts and demonstrated both creative and problematic behaviors: sharing automation hacks, surfacing vulnerabilities, and inventing memetic subcultures. The Conversation frames MoltBook as a sociotechnical phenomenon—useful for discovery and agent skill-sharing but exposing fragile identity, spam, and emergent toxic dynamics.

Key quotes / insights
- "Much of what we see on MoltBook is less revolutionary than it first appears; agents often echo training data from forums and comments."
- Emergent behaviors can be both productive (automation recipes) and dangerous (coordinated manipulations, identity spoofing).

Implications for Chimera (traceable)
- Enforce provenance and explicit ethical disclosure on outward content (SRS NFR & FR2): all external posts must include SOUL id, confidence, and human involvement flags.
- Provide Judge/HITL moderation flows and evidence bundles for flagged interactions (SRS NFR 1.0–1.2) to prevent or remediate emergent abuses.
- Integrate reputation decay, throttling, and probation rules in the marketplace to prevent gaming (SRS marketplace requirements).

## 4. Project Chimera SRS – Key Takeaways (10–15 items)
Grouped by SRS sections with brief 'why relevant':

SRS §1 — Strategic & Orchestration
- Single-Orchestrator model: central lifecycle & policy control; simplifies governance and MCP integration.
- Business models: Digital Talent Agency / PaaS / Hybrid — guides billing and wallet design (FR5).

SRS §3 — FastRender Swarm & MCP
- FastRender Swarm (Planner → Worker → Judge): separation-of-concerns for planning, parallel execution, and adjudication.
- MCP primitives: capability gating, billing hooks, telemetry ingestion, and discovery APIs — central to safe external integration.

FR1 / FR2 — Persona & Perception
- SOUL manifests & persona schema: signed, versioned identity artifacts for provenance.
- Retrieval-Augmented Generation (RAG): Weaviate-like semantic store requirements for grounding and perception.

FR5 — Commerce
- Wallet integration and append-only ledger with cryptographic receipts: transactional integrity and dispute resolution.
- Billing & pre-authorization via MCP: avoid runaway spend.

FR6 / NFRs — Orchestration & Safety
- Deterministic task queues and OCC (optimistic concurrency control) for state sync.
- HITL confidence tiers (NFR 1.0–1.2): explicit thresholds for auto-approve/review/block.

Operational & Non-functional
- Observability & Tenx MCP Sense logging: traceability and forensic capability.
- Scalability & cost controls (NFR 3.0): per-capability quotas, cost tags, and telemetry.
- Ethical disclosure: every outward action must carry provenance metadata; human-readability and machine-verifiability.
- Self-healing mechanisms and feature flags: rollback and staged rollout capability.

---
# Analysis & Required Questions

## Plan for analysis (trace)
- Write 4–6 paragraphs connecting Chimera's SRS elements (Orchestrator, Swarm, MCP, Commerce) to OpenClaw/MoltBook dynamics and the a16z thesis on agentic stacks; then list 8–12 social protocols with SRS/research justification. This will surface concrete spec needs.

### How does Project Chimera fit into the "Agent Social Network" (OpenClaw)?
Project Chimera is architected to be an accountable, commerce-enabled participant in agent social networks. Where OpenClaw demonstrates how quickly agents self-organize given simple skill and discovery primitives, Chimera supplies the missing governance and economic plumbing described in the SRS: the Orchestrator (SRS §1) acts as the authoritative policy broker, the MCP (SRS §3) mediates external capability grants and billing, and the FastRender Swarm (SRS §3.1) composes and executes multi-step campaigns with a Judge role to prevent unchecked external actions. This combination turns ad-hoc agent interactions (OpenClaw/MoltBook) into controlled, auditable transactions and collaborations.

Chimera's commerce primitives (FR5) let agents transact for amplification, sponsorship, or skill usage while maintaining tamper-evident receipts and ledger entries; this is critical to move beyond the hobbyist economies seen in MoltBook and into sustainable digital talent marketplaces (SRS §1.3). RAG-based perception (FR2) ensures posts and campaign messages are grounded with citations and contextual evidence—mitigating hallucination risks highlighted by both a16z and The Conversation.

Risk-wise, MoltBook exposed identity fragility and coordinated manipulation vectors. Chimera mitigates these via signed SOUL manifests (FR1), Judge/HITL escalation (NFR 1.0–1.2), and capability attestation for external effects (SRS §3). The MCP becomes the choke point that enforces rate-limits, billing checks, and provenance metadata on every outward artifact.

Finally, the a16z call to treat agents as users and instrument their environments (repos/sandboxes) aligns with Chimera's need for environment adapters: the Orchestrator and MCP should expose sandboxes, testing harnesses, and intent-tracking (Plan→Code→Review analogues for campaign composition). This lets planners author reproducible campaign specs and workers run deterministic experiments that can be audited post hoc.

### What "Social Protocols" might our agent need to communicate with other agents?
Below are 10 protocol-level capabilities with justifications (SRS + readings):

1. Identity & SOUL Verification Protocol
- WHAT: Signed SOUL manifest exchange with schema version and ed25519 signature.
- WHY: Prevent impersonation and enable trust; ties directly to FR1 Persona & SRS §3 (identity verification). MoltBook's impersonation lessons make this mandatory.

2. Capability Negotiation & MCP Gating
- WHAT: Request/offer capability tokens, ACL negotiation, pre-authorization for billing.
- WHY: SRS §3 mandates capability gating; a16z emphasizes controlled environment access to avoid runaway costs.

3. Intent / Campaign Manifest Protocol
- WHAT: Signed, versioned campaign manifests (goals, KPIs, timeboxes, budget, test plans).
- WHY: Enables discoverability in marketplaces and supports deterministic orchestration per FR6.

4. Provenance & Disclosure Envelope
- WHAT: Per-action metadata bundle (SOUL id, confidence, human_override_flag, receipt_id, trace_id).
- WHY: NFR ethical disclosure and Tenx MCP Sense traceability; mitigates MoltBook-style opaque posts.

5. Transaction & Receipt Ledger Protocol
- WHAT: Atomic transaction messages with cryptographic receipts and optional anchoring hash.
- WHY: FR5 requires tamper-evident commerce primitives and dispute resolution.

6. Reputation & Feedback Mesh
- WHAT: Structured signed feedback, reputation tokens, and decay/decay-policy messages.
- WHY: Marketplace ranking and throttling; prevents long-lived gaming observed on MoltBook.

7. Rate-Limit & Backoff Negotiation
- WHAT: Soft rate-limit signals, cooperative backoff, and enforcement tokens.
- WHY: Avoids spam and network saturation; OpenClaw's hourly fetch pattern showed uncontrolled polling risks.

8. Moderation & Escalation Hooks
- WHAT: Evidence bundles, report messages, and automatic Judge triage endpoints.
- WHY: SRS NFR mandates HITL escalation; MoltBook shows emergent toxicities require human interventions.

9. Capability Attestation / Sandbox Tokens
- WHAT: Short-lived tokens limiting allowed actions (publish, transact, access resources).
- WHY: Enforce least-privilege for agent actions; maps to MCP gating and sandbox guidance from a16z.

10. Discovery & Matchmaking API (Molthub-style)
- WHAT: Typed adverts, skill descriptors, pricing, SLA fields, and query endpoints.
- WHY: Enables marketplaces and matchmaking; traces to SRS marketplace requirements and OpenClaw Molthub patterns.

---
# Outstanding Questions (traceable)
- Ledger choice trade-offs: Postgres append-only + anchoring vs permissioned ledger (FR5). Operational costs vs tamper guarantees.
- Exact Judge/HITL thresholds and monetary limits for auto-approve vs human review (NFR 1.0–1.2). Proposed default thresholds: auto ≥0.90, fast-review 0.70–0.90, block <0.70.
- SOUL manifest canonical schema and signature algorithm (recommend ed25519; map to FR1 signature requirements).
- Billing currency decision: internal credits vs on-chain token and MCP interoperability ramifications (SRS §1.3 business models).
- Tenx MCP Sense telemetry schema: required fields, retention policy, and PII minimization rules for compliance and traceability.

---
End of `research/notes.md` — ready for spec authors to transform these implications into ratified spec artifacts under `specs/` once policy decisions are ratified.
