# Chimera Agent Skills

## Overview

This directory contains **runtime capabilities** (Skills) for Chimera agents. Skills are reusable Python modules that agents call during campaign execution to perform specific tasks.

## What is a Skill?

A **Skill** is a well-defined capability package with:
- **Input/Output Contract**: JSON schema defining expected inputs and outputs
- **Implementation**: Python module with core logic
- **Tests**: Unit tests validating functionality
- **Documentation**: README with usage examples and SRS references

## Skill vs MCP Server

| Aspect | Skill | MCP Server |
|--------|-------|------------|
| **Purpose** | Runtime agent capability | Development-time IDE tool |
| **Used By** | Chimera agents (autonomous) | Developers/IDE (human) |
| **Examples** | fetch_trends, generate_content | git-mcp, database-mcp |
| **Execution** | Called via MCP Gateway with tokens | Called directly by IDE |
| **Location** | `skills/` directory | Installed globally or per-project |

**Critical**: Never confuse Skills with MCP Servers!

## Available Skills

### 1. `skill_fetch_trends`
Retrieve trending topics from social media platforms for campaign targeting.

**SRS Reference**: §4.2 Perception (FR2.2)

**Use Case**: Agent queries Twitter trends before creating campaign content

---

### 2. `skill_generate_content`
Generate campaign content (text, images) using LLM with persona context injection.

**SRS Reference**: §4.3 Creative Engine (FR3.1)

**Use Case**: Agent creates social media post aligned with persona guidelines

---

### 3. `skill_publish_post`
Publish content to social media platforms with provenance metadata.

**SRS Reference**: §4.4 Action System (FR4.2)

**Use Case**: Agent publishes approved content to Twitter with SOUL ID and confidence score

---

### 4. `skill_check_wallet_balance`
Query agent wallet balance and transaction history.

**SRS Reference**: §4.5 Commerce (FR5.1)

**Use Case**: Agent checks budget before purchasing sponsored post placement

---

### 5. `skill_validate_image`
Validate image compliance with brand guidelines and safety policies.

**SRS Reference**: §4.3 Creative Engine (FR3.2)

**Use Case**: Judge validates generated image before external publication

---

## Skill Directory Structure

Each skill follows this structure:

```
skill_<name>/
├── README.md           # Skill documentation
├── skill.py            # Implementation
├── schema.json         # JSON schema for validation
└── tests/
    └── test_<name>.py  # Unit tests
```

## How Agents Use Skills

### 1. Worker Claims Task
```python
task = worker.claim_task_from_queue()
# task_type: "content_generation"
```

### 2. Worker Requests Capability Token
```python
from mcp_client import MCPGateway

gateway = MCPGateway()
token = gateway.request_capability(
    capability_name="generate_content",
    soul_id=worker.soul_id,
    max_spend=5.00
)
```

### 3. Worker Calls Skill via MCP Gateway
```python
result = gateway.call_skill(
    token=token,
    skill_name="generate_content",
    input_data={
        "soul_id": worker.soul_id,
        "content_type": "post",
        "prompt": "Create post about AI trends",
        "context_ids": ["citation:uuid-123"]
    }
)
```

### 4. Worker Submits Result to Judge
```python
worker.submit_to_judge(
    task_id=task.task_id,
    result=result,
    confidence=result["confidence"],
    proof=result["model_metadata"]
)
```

## Skill Development Guidelines

### 1. Input Validation
All skills must validate input against JSON schema:

```python
import jsonschema

def execute_skill(input_data: dict) -> dict:
    # Load schema
    with open("schema.json") as f:
        schema = json.load(f)
    
    # Validate input
    jsonschema.validate(input_data, schema["input"])
    
    # Execute skill logic
    result = perform_skill_logic(input_data)
    
    # Validate output
    jsonschema.validate(result, schema["output"])
    
    return result
```

### 2. Error Handling
Skills must handle errors gracefully:

```python
try:
    result = api_call(input_data)
except APIError as e:
    return {
        "status": "FAILED",
        "error": {
            "error_code": "API_ERROR",
            "error_message": str(e)
        }
    }
```

### 3. Telemetry
Skills must emit telemetry events:

```python
from task1.telemetry import emit_event

emit_event(
    event_type="skill.executed",
    skill_name="fetch_trends",
    trace_id=trace_id,
    metadata={"platform": "twitter", "trend_count": 5}
)
```

### 4. Testing
Each skill must have comprehensive unit tests:

```python
def test_fetch_trends_success():
    input_data = {
        "platform": "twitter",
        "category": "tech",
        "limit": 5
    }
    
    result = fetch_trends.execute_skill(input_data)
    
    assert "trends" in result
    assert len(result["trends"]) <= 5
    assert all("topic" in t for t in result["trends"])
```

## Skill Registration

Skills are registered in the MCP Gateway capability registry:

```python
# mcp_gateway/capability_registry.py

SKILL_REGISTRY = {
    "fetch_trends": {
        "skill_module": "skills.skill_fetch_trends.skill",
        "cost_per_call": 0.10,
        "rate_limit": {"calls_per_hour": 100}
    },
    "generate_content": {
        "skill_module": "skills.skill_generate_content.skill",
        "cost_per_call": 0.50,
        "rate_limit": {"calls_per_hour": 50}
    },
    # ... other skills
}
```

## Security Considerations

1. **Capability Tokens**: All skill calls require valid capability tokens
2. **Input Sanitization**: Skills must sanitize inputs to prevent injection attacks
3. **Rate Limiting**: MCP Gateway enforces per-skill rate limits
4. **Budget Checks**: Pre-authorization prevents exceeding agent budgets
5. **Audit Logging**: All skill calls logged to telemetry

## Future Skills

Planned skills for future implementation:
- `skill_analyze_sentiment`: Analyze sentiment of social media posts
- `skill_schedule_campaign`: Schedule multi-step campaign execution
- `skill_fetch_analytics`: Retrieve campaign performance metrics
- `skill_negotiate_price`: Negotiate pricing with external agents
- `skill_verify_identity`: Verify SOUL manifest signatures

---

**Document Status**: v1.0  
**Last Updated**: 2026-02-06  
**Owner**: Skills Team
