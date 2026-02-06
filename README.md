# Project Chimera: Autonomous Influencer Network

> **A FastRender Swarm Implementation with MCP & Agentic Commerce**

[![CI/CD Pipeline](https://github.com/ruthasoll/The-Agentic-Infrastructure-Challenge-/actions/workflows/main.yml/badge.svg)](https://github.com/ruthasoll/The-Agentic-Infrastructure-Challenge-/actions/workflows/main.yml)
[![TDD Compliance](https://img.shields.io/badge/TDD-Strict-green)](.cursor/rules)
[![Spec-First](https://img.shields.io/badge/Governance-Spec--First-blue)](specs/)

Project Chimera is an advanced agentic infrastructure designed to create, manage, and scale autonomous AI influencers. Built on the **FastRender Swarm** architecture, it leverages **Model Context Protocol (MCP)** for secure tool integration and **Agentic Commerce** for autonomous value exchange.

---

## 🏗️ System Architecture

### 1. FastRender Swarm (The Brain)
- **Planner**: Decomposes high-level campaigns into atomic tasks (DAGs).
- **Worker**: Stateless execution units that claim tasks from Redis.
- **Judge**: QA layer ensuring brand safety and hallucinaton checks.
- **Orchestrator**: Manages agent lifecycle (Creation, Activation, Suspension).

### 2. MCP Gateway (The Hands)
All external interactions (Social Media, Wallets, Browsing) are mediated through the **MCP Gateway**.
- **Security**: No direct API keys in agent code. Capability tokens only.
- **Billing**: Granular cost tracking per agent/campaign.
- **Telemetry**: Full observability via Tenx Sense.

### 3. Agent Skills (The Capabilities)
Modular, verified capabilities that agents can invoke:
- `fetch_trends`: Real-time social signal analysis.
- `generate_content`: Multi-modal content creation.
- `publish_post`: Cross-platform publishing with provenance.
- `check_wallet_balance`: Financial awareness.
- `validate_image`: Brand safety compliance.

---

## 🛡️ Governance & Development Rules

We subscribe to **Strict Governance** to prevent AI hallucination and ensure reliability.

### 📜 The Prime Directive
> **"NEVER generate code without a committed spec."**

1.  **Spec-First**: Implementation (`src/`) must trace back to Specifications (`specs/`) and SRS.
2.  **True TDD**: Write failing tests (`tests/`) *before* any implementation code.
3.  **Traceability**: Every file must reference its SRS section.
    ```python
    """
    SRS Reference: §4.2 Perception
    Spec: specs/functional.md, FR2.1
    """
    ```

See [.cursor/rules](.cursor/rules) for the full rulebook.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Docker & Docker Compose
- Windows (Powershell) or Linux/Mac

### 🛠️ Developer Tools (`build.ps1`)
We use a unified build script for cross-platform automation.

| Command | Description |
|---------|-------------|
| `.\build.ps1 setup` | Install dependencies (`uv` or `pip`) |
| `.\build.ps1 test` | Run all tests with coverage (TDD) |
| `.\build.ps1 spec-check` | **Governance**: Verify spec references in code |
| `.\build.ps1 lint` | Auto-format (`black`) and lint (`ruff`) |
| `.\build.ps1 docker-build`| Build production Docker image |

### 🔨 Daily Workflow

1.  **Pick a Task**: Check `tasks.md` or Jira.
2.  **Update Spec**: Modify `specs/*.md` if requirements change.
3.  **Write Test**: Create `tests/test_feature.py`.
    ```powershell
    .\build.ps1 test  # Must Fail 🔴
    ```
4.  **Implement**: Write code in `src/`.
5.  **Verify**:
    ```powershell
    .\build.ps1 test  # Must Pass 🟢
    .\build.ps1 lint  # Code Quality
    .\build.ps1 spec-check # Traceability
    ```
6.  **Commit**: Push to GitHub (CI/CD will verify).

---

## 📂 Project Structure

```
├── .cursor/rules           # 🚨 AI Agent Governance Rules (READ THIS)
├── .github/workflows/      # CI/CD Pipeline (Test, Lint, Security, Governance)
├── build.ps1               # Automation Script (Windows)
├── Makefile                # Automation Script (Linux/Mac)
├── Dockerfile              # Multi-stage production build
├── specs/                  # 📚 SOURCE OF TRUTH
│   ├── functional.md       # Functional Requirements (User Stories)
│   ├── technical.md        # JSON Schemas & API Contracts
│   └── openclaw_integration.md
├── src/                    # Implementation Code
│   ├── schemas/            # Pydantic/JSON Schemas
│   └── orchestrator/       # Core System Components
├── skills/                 # 🧩 Runtime Agent Capabilities
│   ├── skill_fetch_trends/
│   └── skill_publish_post/
└── tests/                  # 🧪 Test Suite (Mirror of src/)
```

---

## 🤖 CI/CD & AI Review

Every PR is automatically reviewed by **CodeRabbit** and **GitHub Actions**:

1.  **Spec Check**: Does the code match the spec?
2.  **TDD Check**: Do tests exist for the new code?
3.  **Security**: Are there hardcoded secrets? (Blocked!)
4.  **Quality**: Type hints, docstrings, and complexity.

---

**Project Chimera** — *Building the future of Autonomous Agentic Commerce.*