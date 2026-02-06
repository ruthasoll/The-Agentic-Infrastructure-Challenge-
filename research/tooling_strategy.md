# Tooling & Skills Strategy — Project Chimera

## Overview

This document defines the tooling and skills strategy for Project Chimera, separating **developer tools (MCP Servers)** from **runtime agent capabilities (Skills)**.

**Key Distinction**:
- **MCP Servers**: Development-time tools for IDE/developers (YOU/me)
- **Skills**: Runtime capabilities for Chimera agents (autonomous influencers)

---

## A. Developer Tools (MCP Servers for IDE)

MCP Servers extend the IDE with specialized capabilities for development, testing, and deployment. These are **NOT** used by Chimera agents at runtime.

### 1. Git MCP Server

**Purpose**: Git operations and version control integration

**How It Helps Development**:
- Automated commit message generation with spec references
- Branch management for feature development
- Git history analysis for traceability
- Pre-commit hooks for spec validation

**Install Command**:
```bash
npm install -g @modelcontextprotocol/server-git
```

**Configuration** (`.antigravity/mcp.json`):
```json
{
  "servers": {
    "git": {
      "command": "mcp-server-git",
      "args": ["--repo", "."],
      "type": "stdio"
    }
  }
}
```

**Use Cases**:
- Generate atomic commits with spec references
- Verify spec files are committed before implementation
- Track which specs have been implemented

---

### 2. Filesystem MCP Server

**Purpose**: Enhanced file system operations and code navigation

**How It Helps Development**:
- Smart file search across project structure
- Batch file operations (create multiple test files)
- File watching for spec changes
- Directory structure validation

**Install Command**:
```bash
npm install -g @modelcontextprotocol/server-filesystem
```

**Configuration**:
```json
{
  "servers": {
    "filesystem": {
      "command": "mcp-server-filesystem",
      "args": ["--allowed-directories", ".", "--watch"],
      "type": "stdio"
    }
  }
}
```

**Use Cases**:
- Verify `specs/` directory structure
- Create test files matching spec acceptance criteria
- Monitor spec file changes for re-implementation

---

### 3. GitHub MCP Server

**Purpose**: GitHub API integration for issues, PRs, and project management

**How It Helps Development**:
- Create issues from spec acceptance criteria
- Link PRs to spec files automatically
- Track implementation progress via GitHub Projects
- Automated PR descriptions with spec references

**Install Command**:
```bash
npm install -g @modelcontextprotocol/server-github
```

**Configuration**:
```json
{
  "servers": {
    "github": {
      "command": "mcp-server-github",
      "args": ["--token", "${GITHUB_TOKEN}"],
      "type": "stdio",
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

**Use Cases**:
- Create GitHub issues for each spec section
- Generate PR templates with spec traceability
- Track spec implementation status in GitHub Projects

---

### 4. Database MCP Server

**Purpose**: Database schema management and query execution

**How It Helps Development**:
- Generate PostgreSQL migrations from `specs/technical.md`
- Validate database schema against spec
- Run test queries for integration tests
- Seed test data for TDD

**Install Command**:
```bash
npm install -g @modelcontextprotocol/server-postgres
```

**Configuration**:
```json
{
  "servers": {
    "database": {
      "command": "mcp-server-postgres",
      "args": [
        "--connection-string",
        "postgresql://localhost:5432/chimera_dev"
      ],
      "type": "stdio"
    }
  }
}
```

**Use Cases**:
- Create PostgreSQL tables from `specs/technical.md` schema
- Generate test fixtures for campaign and agent data
- Validate ledger append-only constraints

**SRS Reference**: §4.5 Commerce (FR5), `specs/technical.md` Database Schema

---

### 5. Playwright MCP Server

**Purpose**: Browser automation for testing web interfaces

**How It Helps Development**:
- Automated UI testing for dashboard
- Screenshot generation for documentation
- End-to-end testing of agent workflows
- Visual regression testing

**Install Command**:
```bash
npm install -g @modelcontextprotocol/server-playwright
```

**Configuration**:
```json
{
  "servers": {
    "playwright": {
      "command": "mcp-server-playwright",
      "args": ["--browser", "chromium"],
      "type": "stdio"
    }
  }
}
```

**Use Cases**:
- Test campaign creation UI flows
- Validate agent dashboard displays correct metrics
- Capture screenshots for walkthrough documentation

---

### 6. Weaviate MCP Server (Custom)

**Purpose**: Vector database operations for RAG testing

**How It Helps Development**:
- Seed persona embeddings for testing
- Validate RAG retrieval queries
- Test citation similarity scoring
- Benchmark vector search performance

**Install Command**:
```bash
# Custom MCP server (to be implemented)
pip install mcp-server-weaviate
```

**Configuration**:
```json
{
  "servers": {
    "weaviate": {
      "command": "mcp-server-weaviate",
      "args": ["--url", "http://localhost:8080"],
      "type": "stdio"
    }
  }
}
```

**Use Cases**:
- Create test persona embeddings
- Validate RAG queries return similarity ≥ 0.75
- Test citation retrieval for content generation

**SRS Reference**: §4.2 Perception (FR2), `specs/technical.md` Weaviate Collections

---

## B. Agent Skills (Runtime Capabilities)

Skills are reusable capability packages that Chimera agents call during campaign execution. Each skill has a well-defined input/output contract.

**Skill Definition**: A skill is a Python module with:
- `README.md`: Documentation and contract
- `skill.py`: Implementation
- `schema.json`: JSON schema for input/output validation
- `tests/`: Unit tests

---

### Skill 1: `fetch_trends`

**Description**: Retrieve trending topics from social media platforms for campaign targeting.

**SRS Reference**: §4.2 Perception (FR2.2 Campaign Context Enrichment)

**Input Contract**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `platform` | string | Yes | Social platform (twitter, instagram, tiktok) |
| `category` | string | No | Topic category (tech, fashion, sports) |
| `region` | string | No | Geographic region (US, EU, GLOBAL) |
| `limit` | integer | No | Max trends to return (default: 10) |

**Input Example**:
```json
{
  "platform": "twitter",
  "category": "tech",
  "region": "US",
  "limit": 5
}
```

**Output Contract**:

| Field | Type | Description |
|-------|------|-------------|
| `trends` | array | List of trending topics |
| `trends[].topic` | string | Trending topic/hashtag |
| `trends[].volume` | integer | Tweet/post volume |
| `trends[].sentiment` | number | Sentiment score (-1.0 to 1.0) |
| `trends[].retrieved_at` | string | ISO 8601 timestamp |

**Output Example**:
```json
{
  "trends": [
    {
      "topic": "#AI2026",
      "volume": 125000,
      "sentiment": 0.72,
      "retrieved_at": "2026-02-06T16:50:00Z"
    },
    {
      "topic": "#TechInnovation",
      "volume": 98000,
      "sentiment": 0.85,
      "retrieved_at": "2026-02-06T16:50:00Z"
    }
  ]
}
```

**Dependencies**: Twitter API v2, MCP Gateway capability token

---

### Skill 2: `generate_content`

**Description**: Generate campaign content (text, images) using LLM with persona context injection.

**SRS Reference**: §4.3 Creative Engine (FR3.1 AI-Generated Campaign Content)

**Input Contract**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `soul_id` | string | Yes | Agent SOUL ID for persona context |
| `content_type` | string | Yes | Type (post, image, video) |
| `prompt` | string | Yes | Content generation prompt |
| `context_ids` | array | No | Citation source IDs for RAG |
| `max_length` | integer | No | Max content length (chars/tokens) |

**Input Example**:
```json
{
  "soul_id": "chimera:agent:uuid-123",
  "content_type": "post",
  "prompt": "Create a post about AI trends in 2026",
  "context_ids": ["citation:uuid-456", "citation:uuid-789"],
  "max_length": 280
}
```

**Output Contract**:

| Field | Type | Description |
|-------|------|-------------|
| `content` | string | Generated content |
| `confidence` | number | Model confidence (0.0-1.0) |
| `citations` | array | Citation metadata |
| `citations[].source_id` | string | Citation source ID |
| `citations[].similarity_score` | number | RAG similarity score |
| `model_metadata` | object | Model name, prompt hash |
| `generated_at` | string | ISO 8601 timestamp |

**Output Example**:
```json
{
  "content": "🚀 AI in 2026 is transforming industries! From autonomous agents to creative tools, the future is here. #AI2026 #Innovation",
  "confidence": 0.87,
  "citations": [
    {
      "source_id": "citation:uuid-456",
      "similarity_score": 0.82
    }
  ],
  "model_metadata": {
    "model_name": "gpt-4-turbo",
    "prompt_hash": "sha256:abc123..."
  },
  "generated_at": "2026-02-06T16:55:00Z"
}
```

**Dependencies**: OpenAI API, Weaviate (RAG), MCP Gateway

---

### Skill 3: `publish_post`

**Description**: Publish content to social media platforms with provenance metadata.

**SRS Reference**: §4.4 Action System (FR4.2 External API Integration)

**Input Contract**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `platform` | string | Yes | Target platform (twitter, instagram) |
| `content` | string | Yes | Post content |
| `media_urls` | array | No | Media asset URLs |
| `schedule_at` | string | No | ISO 8601 timestamp for scheduling |
| `provenance` | object | Yes | Provenance metadata bundle |

**Input Example**:
```json
{
  "platform": "twitter",
  "content": "🚀 AI in 2026 is transforming industries!",
  "media_urls": ["https://s3.example.com/image123.png"],
  "schedule_at": null,
  "provenance": {
    "soul_id": "chimera:agent:uuid-123",
    "confidence": 0.87,
    "human_override_flag": false,
    "trace_id": "trace_abc123:evt42"
  }
}
```

**Output Contract**:

| Field | Type | Description |
|-------|------|-------------|
| `post_id` | string | Platform post ID |
| `post_url` | string | Public URL to post |
| `published_at` | string | ISO 8601 timestamp |
| `receipt_id` | string | Transaction receipt ID |
| `status` | string | SUCCESS, FAILED, SCHEDULED |

**Output Example**:
```json
{
  "post_id": "twitter:1234567890",
  "post_url": "https://twitter.com/chimera_agent/status/1234567890",
  "published_at": "2026-02-06T17:00:00Z",
  "receipt_id": "receipt:uuid-999",
  "status": "SUCCESS"
}
```

**Dependencies**: Twitter API, Instagram API, MCP Gateway, PostgreSQL (ledger)

---

### Skill 4: `check_wallet_balance`

**Description**: Query agent wallet balance and transaction history.

**SRS Reference**: §4.5 Commerce (FR5.1 Secure Wallet Integration)

**Input Contract**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `soul_id` | string | Yes | Agent SOUL ID |
| `include_pending` | boolean | No | Include pending transactions |

**Input Example**:
```json
{
  "soul_id": "chimera:agent:uuid-123",
  "include_pending": true
}
```

**Output Contract**:

| Field | Type | Description |
|-------|------|-------------|
| `balance` | number | Current balance |
| `currency` | string | Currency code (USD) |
| `pending_balance` | number | Pending transactions total |
| `recent_transactions` | array | Last 10 transactions |
| `recent_transactions[].tx_id` | string | Transaction ID |
| `recent_transactions[].amount` | number | Transaction amount |
| `recent_transactions[].purpose` | string | Transaction purpose |

**Output Example**:
```json
{
  "balance": 475.50,
  "currency": "USD",
  "pending_balance": 25.00,
  "recent_transactions": [
    {
      "tx_id": "tx:uuid-111",
      "amount": -25.00,
      "purpose": "Campaign collaboration payment",
      "created_at": "2026-02-06T16:50:00Z"
    }
  ]
}
```

**Dependencies**: PostgreSQL (ledger table)

---

### Skill 5: `validate_image`

**Description**: Validate image compliance with brand guidelines and safety policies.

**SRS Reference**: §4.3 Creative Engine (FR3.2 Content Quality Assurance)

**Input Contract**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `image_url` | string | Yes | URL to image asset |
| `brand_guidelines` | object | Yes | Brand guideline rules |
| `brand_guidelines.allowed_colors` | array | No | Hex color codes |
| `brand_guidelines.prohibited_content` | array | No | Prohibited content types |

**Input Example**:
```json
{
  "image_url": "https://s3.example.com/image123.png",
  "brand_guidelines": {
    "allowed_colors": ["#FF5733", "#3498DB"],
    "prohibited_content": ["violence", "nudity"]
  }
}
```

**Output Contract**:

| Field | Type | Description |
|-------|------|-------------|
| `is_valid` | boolean | Validation result |
| `confidence` | number | Validation confidence (0.0-1.0) |
| `violations` | array | List of violations |
| `violations[].type` | string | Violation type |
| `violations[].severity` | string | HIGH, MEDIUM, LOW |
| `violations[].description` | string | Violation details |

**Output Example**:
```json
{
  "is_valid": false,
  "confidence": 0.92,
  "violations": [
    {
      "type": "color_mismatch",
      "severity": "MEDIUM",
      "description": "Image contains color #000000 not in allowed palette"
    }
  ]
}
```

**Dependencies**: Computer Vision API, MCP Gateway

---

## Skill Directory Structure

```
skills/
├── README.md                           # Overview of skills system
├── skill_fetch_trends/
│   ├── README.md                       # Skill documentation
│   ├── skill.py                        # Implementation
│   ├── schema.json                     # JSON schema
│   └── tests/
│       └── test_fetch_trends.py
├── skill_generate_content/
│   ├── README.md
│   ├── skill.py
│   ├── schema.json
│   └── tests/
├── skill_publish_post/
│   ├── README.md
│   ├── skill.py
│   ├── schema.json
│   └── tests/
├── skill_check_wallet_balance/
│   ├── README.md
│   ├── skill.py
│   ├── schema.json
│   └── tests/
└── skill_validate_image/
    ├── README.md
    ├── skill.py
    ├── schema.json
    └── tests/
```

---

## Implementation Guidelines

### MCP Servers (Developer Tools)
1. Install MCP servers globally or per-project
2. Configure in `.antigravity/mcp.json` or `.vscode/mcp.json`
3. Use during development for automation and testing
4. **Never** call MCP servers from runtime agent code

### Skills (Runtime Capabilities)
1. Implement each skill as a Python module
2. Define JSON schemas for input/output validation
3. Write comprehensive tests for each skill
4. Register skills in agent capability registry
5. Call skills through MCP Gateway with capability tokens

---

**Document Status**: Draft v1.0  
**Owner**: Architecture Team  
**Last Updated**: 2026-02-06  
**Next Review**: After skills/ directory implementation
