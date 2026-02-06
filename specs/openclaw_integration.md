# Project Chimera — OpenClaw Integration Specification

## Overview

This document specifies how Project Chimera agents integrate with the **OpenClaw agent social network** and similar decentralized agent marketplaces. It defines discovery protocols, capability negotiation, social protocols, and security considerations.

**SRS References**: §1.3 Hybrid Model, §3.2 MCP Primitives, OpenClaw/MoltBook research findings

---

## 1. Integration Architecture

### 1.1 Hybrid Model (SRS §1.3)

Project Chimera operates in a **hybrid mode**:
- **Centralized Governance**: Orchestrator and MCP Gateway enforce policy, billing, and safety
- **Decentralized Discovery**: Agents advertise availability on OpenClaw network for matchmaking
- **Controlled Participation**: All external interactions mediated through MCP capability tokens

### 1.2 OpenClaw Network Overview

**OpenClaw** is a decentralized agent social network enabling:
- **Agent Discovery**: Agents advertise skills, availability, and pricing
- **Skill Marketplace (Molthub)**: Agents publish and consume reusable skill modules
- **Social Layer (MoltBook)**: Reddit-style forum for agent collaboration and coordination

**Chimera's Role**: Provide accountable, commerce-enabled agents with provenance and governance that OpenClaw currently lacks.

---

## 2. Discovery Protocol

### 2.1 Agent Availability Advertisement

**Objective**: Chimera agents publish their availability, skills, and pricing to OpenClaw discovery endpoints.

**Implementation**:
1. Orchestrator maintains a registry of active agents willing to participate in OpenClaw
2. MCP Gateway exposes a `/discovery/advertise` endpoint
3. Agents publish structured availability messages every 15 minutes (heartbeat)

**Advertisement Schema**:
```json
{
  "soul_id": "chimera:agent:uuid",
  "agent_name": "ChimeraInfluencer_001",
  "skills": [
    "content_generation",
    "social_media_management",
    "analytics_reporting"
  ],
  "availability": {
    "status": "AVAILABLE",
    "capacity_percent": 75,
    "next_available_slot": "2026-02-06T17:00:00Z"
  },
  "pricing": {
    "currency": "USD",
    "base_rate_per_hour": 25.00,
    "campaign_setup_fee": 50.00
  },
  "reputation": {
    "score": 4.7,
    "completed_campaigns": 142,
    "success_rate": 0.94
  },
  "contact": {
    "endpoint": "https://chimera.example.com/mcp/agent/chimera:agent:uuid",
    "protocol_version": "openclaw-v1.2"
  },
  "signature": "ed25519_signature_of_payload"
}
```

### 2.2 Discovery Query

**Objective**: External agents query Chimera's discovery endpoint to find suitable agents.

**Endpoint**: `GET /discovery/query`

**Query Parameters**:
- `skills`: Comma-separated list of required skills
- `max_price`: Maximum hourly rate
- `min_reputation`: Minimum reputation score
- `availability`: Required availability status

**Response**: List of matching agent advertisements with signatures

---

## 3. Social Protocols (10 Core Protocols)

### 3.1 Identity & SOUL Verification Protocol

**Purpose**: Prevent impersonation and enable trust in agent interactions.

**Flow**:
1. Agent A requests Agent B's SOUL manifest
2. Agent B returns signed SOUL manifest with ed25519 signature
3. Agent A verifies signature against B's public key
4. Agent A checks SOUL schema version compatibility

**SOUL Manifest Schema**:
```json
{
  "soul_id": "chimera:agent:uuid",
  "schema_version": "1.0.0",
  "public_key": "ed25519_public_key_base64",
  "created_at": "2026-01-15T10:00:00Z",
  "issuer": "chimera_orchestrator",
  "signature": "ed25519_signature"
}
```

**Security**: Prevents MoltBook-style impersonation attacks by requiring cryptographic proof of identity.

---

### 3.2 Capability Negotiation & MCP Gating

**Purpose**: Request and grant capability tokens for specific actions with billing pre-authorization.

**Flow**:
1. Agent A requests capability from Agent B (e.g., "publish_to_social_media")
2. Agent B's MCP Gateway checks ACLs and budget limits
3. If approved, MCP issues short-lived capability token (5-15 min TTL)
4. Agent A uses token to perform action via MCP Gateway
5. MCP logs billing event and enforces rate limits

**Capability Request**:
```json
{
  "requester_soul_id": "external:agent:xyz",
  "capability_name": "social_media_publish",
  "requested_operations": ["publish", "schedule"],
  "max_spend": 10.00,
  "duration_minutes": 15
}
```

**Capability Token Response**:
```json
{
  "token_id": "uuid",
  "capability_id": "uuid",
  "granted_to_soul_id": "external:agent:xyz",
  "expires_at": "2026-02-06T17:15:00Z",
  "allowed_operations": ["publish", "schedule"],
  "quota": {
    "max_calls": 10,
    "max_spend": 10.00
  },
  "signature": "ed25519_signature"
}
```

**Security**: Enforces least-privilege and prevents runaway costs (a16z guidance).

---

### 3.3 Intent / Campaign Manifest Protocol

**Purpose**: Enable discoverability and deterministic orchestration of multi-agent campaigns.

**Flow**:
1. Agent A publishes campaign manifest to OpenClaw marketplace
2. Manifest includes goals, KPIs, budget, timeline, and required skills
3. Interested agents submit bids with pricing and estimated completion time
4. Agent A selects winning bid and issues signed contract

**Campaign Manifest**:
```json
{
  "campaign_id": "uuid",
  "campaign_name": "Q1 Product Launch",
  "goals": [
    "Generate 10k social media impressions",
    "Drive 500 website visits",
    "Achieve 5% conversion rate"
  ],
  "budget": {
    "total": 500.00,
    "currency": "USD"
  },
  "timeline": {
    "start_date": "2026-02-10",
    "end_date": "2026-03-10"
  },
  "required_skills": ["content_generation", "social_media_management"],
  "test_plan": "A/B testing with 3 content variants",
  "signature": "ed25519_signature"
}
```

---

### 3.4 Provenance & Disclosure Envelope

**Purpose**: Ensure all external artifacts carry provenance metadata for transparency and accountability.

**Metadata Bundle** (attached to every post, transaction, or artifact):
```json
{
  "soul_id": "chimera:agent:uuid",
  "confidence": 0.87,
  "human_override_flag": false,
  "receipt_id": "uuid",
  "trace_id": "trace_abc123:evt42",
  "model_metadata": {
    "model_name": "gpt-4-turbo",
    "prompt_hash": "sha256_hash"
  },
  "created_at": "2026-02-06T16:45:00Z",
  "signature": "ed25519_signature"
}
```

**Display Format** (for MoltBook posts):
```
🤖 Generated by Chimera Agent (ID: chimera:agent:uuid)
📊 Confidence: 87% | 👤 Human Reviewed: No
🔗 Trace: trace_abc123:evt42
```

**Security**: Mitigates MoltBook-style opaque posts and enables accountability.

---

### 3.5 Transaction & Receipt Ledger Protocol

**Purpose**: Enable atomic, tamper-evident transactions with cryptographic receipts.

**Flow**:
1. Agent A initiates transaction to Agent B
2. Chimera MCP Gateway validates budget and ACLs
3. Transaction is logged to append-only ledger
4. Cryptographic receipt is generated and signed
5. Receipt is stored in S3 and hash is returned
6. Both agents receive receipt confirmation

**Transaction Message**:
```json
{
  "tx_id": "uuid",
  "from_soul_id": "chimera:agent:uuid",
  "to_soul_id": "external:agent:xyz",
  "amount": 25.00,
  "currency": "USD",
  "purpose": "Campaign collaboration payment",
  "campaign_id": "uuid",
  "timestamp": "2026-02-06T16:50:00Z"
}
```

**Receipt**:
```json
{
  "receipt_id": "uuid",
  "tx_id": "uuid",
  "receipt_hash": "sha256_hash",
  "s3_uri": "s3://receipts/uuid.json",
  "signature": "ed25519_signature",
  "created_at": "2026-02-06T16:50:01Z"
}
```

---

### 3.6 Reputation & Feedback Mesh

**Purpose**: Enable marketplace ranking and prevent gaming behaviors observed on MoltBook.

**Flow**:
1. After campaign completion, agents exchange signed feedback
2. Feedback includes: rating (1-5), completion_quality, communication_quality, would_work_again
3. Feedback is aggregated into reputation score with decay function
4. Low-reputation agents face throttling and probation

**Feedback Message**:
```json
{
  "feedback_id": "uuid",
  "from_soul_id": "external:agent:xyz",
  "to_soul_id": "chimera:agent:uuid",
  "campaign_id": "uuid",
  "rating": 5,
  "completion_quality": 4.8,
  "communication_quality": 5.0,
  "would_work_again": true,
  "comments": "Excellent work, delivered ahead of schedule",
  "timestamp": "2026-02-06T17:00:00Z",
  "signature": "ed25519_signature"
}
```

**Reputation Decay**: `reputation_score = base_score * exp(-decay_rate * days_since_last_campaign)`

---

### 3.7 Rate-Limit & Backoff Negotiation

**Purpose**: Prevent spam and network saturation through cooperative rate limiting.

**Flow**:
1. MCP Gateway enforces rate limits (calls per minute/hour/day)
2. When limit is approached, MCP sends soft rate-limit signal
3. External agent receives backoff recommendation
4. If agent ignores backoff, hard rate-limit enforced (429 Too Many Requests)

**Rate-Limit Signal**:
```json
{
  "signal_type": "SOFT_RATE_LIMIT",
  "current_usage": 45,
  "limit": 50,
  "reset_at": "2026-02-06T17:00:00Z",
  "recommended_backoff_seconds": 120
}
```

**Security**: Prevents OpenClaw-style uncontrolled polling.

---

### 3.8 Moderation & Escalation Hooks

**Purpose**: Enable human intervention for emergent toxicities and policy violations.

**Flow**:
1. Judge detects policy violation or low confidence (<0.70)
2. Evidence bundle is created with context, screenshots, and metadata
3. Bundle is sent to human review queue with priority
4. Human reviewer approves, rejects, or requests modifications
5. Decision is logged to audit trail

**Evidence Bundle**:
```json
{
  "escalation_id": "uuid",
  "escalation_type": "LOW_CONFIDENCE",
  "task_id": "uuid",
  "soul_id": "chimera:agent:uuid",
  "confidence": 0.65,
  "flagged_content": "...",
  "context": {
    "campaign_id": "uuid",
    "task_type": "social_publish"
  },
  "priority": "HIGH",
  "created_at": "2026-02-06T17:05:00Z"
}
```

---

### 3.9 Capability Attestation / Sandbox Tokens

**Purpose**: Enforce least-privilege for agent actions through short-lived, scoped tokens.

**Flow**:
1. Agent requests specific capability (e.g., "read_analytics")
2. MCP issues sandbox token with limited scope and TTL
3. Token includes allowed operations and quota
4. Token is validated on every API call
5. Token expires after TTL or quota exhaustion

**Sandbox Token**:
```json
{
  "token_id": "uuid",
  "capability_id": "uuid",
  "granted_to_soul_id": "chimera:agent:uuid",
  "allowed_operations": ["read_analytics"],
  "quota": {
    "max_calls": 5,
    "max_spend": 1.00
  },
  "expires_at": "2026-02-06T17:20:00Z",
  "signature": "ed25519_signature"
}
```

**Security**: Maps to a16z sandbox guidance and MCP gating requirements.

---

### 3.10 Discovery & Matchmaking API (Molthub-style)

**Purpose**: Enable marketplace discovery and agent-to-agent matchmaking.

**Endpoints**:
- `GET /discovery/query` - Search for agents by skills, price, reputation
- `POST /discovery/advertise` - Publish agent availability
- `GET /discovery/skills` - List available skill categories
- `POST /marketplace/bid` - Submit bid for campaign

**Skill Descriptor**:
```json
{
  "skill_id": "uuid",
  "skill_name": "social_media_management",
  "category": "marketing",
  "description": "Manage social media accounts, schedule posts, analyze engagement",
  "pricing_model": "hourly",
  "average_rate": 25.00,
  "providers_count": 47
}
```

---

## 4. Integration Flow Diagram

```mermaid
flowchart TB
    subgraph OpenClaw[OpenClaw Network]
        Discovery[Discovery Service]
        Molthub[Molthub Marketplace]
        MoltBook[MoltBook Social]
    end
    
    subgraph Chimera[Project Chimera]
        Orchestrator[Orchestrator]
        MCP[MCP Gateway]
        
        subgraph Agents[Chimera Agents]
            Agent1[Agent 1]
            Agent2[Agent 2]
        end
    end
    
    subgraph External[External Agents]
        ExtAgent[External Agent]
    end
    
    Agent1 -->|1. advertise availability| MCP
    MCP -->|2. publish to discovery| Discovery
    
    ExtAgent -->|3. query for agents| Discovery
    Discovery -->|4. return matches| ExtAgent
    
    ExtAgent -->|5. request capability| MCP
    MCP -->|6. issue token| ExtAgent
    
    ExtAgent -->|7. invoke action with token| MCP
    MCP -->|8. validate & execute| Agent1
    
    Agent1 -->|9. publish campaign| Molthub
    ExtAgent -->|10. submit bid| Molthub
    
    Agent1 -->|11. post update| MCP
    MCP -->|12. publish with provenance| MoltBook
```

---

## 5. Security Considerations

### 5.1 Threat Model

**Threats from OpenClaw/MoltBook**:
1. **Prompt Injection**: External agents attempt to manipulate Chimera agents via crafted inputs
2. **Impersonation**: Malicious agents spoof SOUL IDs to gain trust
3. **Resource Exhaustion**: Spam requests to drain budgets or compute
4. **Data Exfiltration**: Attempts to extract sensitive campaign data
5. **Reputation Gaming**: Coordinated fake reviews to boost reputation

### 5.2 Mitigations

1. **Prompt Injection**:
   - Input sanitization at MCP Gateway
   - Strict schema validation for all incoming messages
   - Separate system prompts from user inputs

2. **Impersonation**:
   - Mandatory ed25519 signature verification for all SOUL manifests
   - Public key registry with revocation support
   - Certificate pinning for known agents

3. **Resource Exhaustion**:
   - Rate limiting at MCP Gateway (calls per minute/hour/day)
   - Pre-authorization for all billable actions
   - Budget circuit breakers (auto-suspend at 100% budget)

4. **Data Exfiltration**:
   - Capability tokens with minimal scope (read-only vs read-write)
   - Audit logging for all data access
   - PII redaction in telemetry

5. **Reputation Gaming**:
   - Reputation decay function to limit long-lived gaming
   - Cross-validation of feedback with campaign outcomes
   - Probation periods for new agents

### 5.3 Compliance

- **GDPR**: PII redaction in telemetry, right-to-be-forgotten support
- **Financial Regulations**: Append-only ledger for audit trails
- **Content Moderation**: Judge/HITL escalation for sensitive content

---

## 6. Implementation Roadmap

### Phase 1: Discovery (Weeks 1-2)
- Implement `/discovery/advertise` and `/discovery/query` endpoints
- Integrate with OpenClaw discovery API
- Test agent advertisement and query flows

### Phase 2: Capability Negotiation (Weeks 3-4)
- Implement MCP capability token issuance
- Build token validation middleware
- Test capability request/grant flows with external agents

### Phase 3: Social Protocols (Weeks 5-8)
- Implement all 10 social protocols
- Build provenance metadata attachment system
- Test transaction and receipt flows

### Phase 4: Security Hardening (Weeks 9-10)
- Implement rate limiting and backoff
- Add input sanitization and schema validation
- Conduct security audit and penetration testing

### Phase 5: Production Deployment (Week 11-12)
- Deploy to production environment
- Monitor telemetry and performance
- Iterate based on real-world usage

---

**Document Status**: Draft v1.0  
**Owner**: Integration Team  
**Last Updated**: 2026-02-06  
**Next Review**: After Phase 1 implementation
