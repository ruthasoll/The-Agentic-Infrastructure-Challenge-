# Frontend Specification: Agent Command Center

## 1. Overview
The **Agent Command Center** is a web-based dashboard for human operators to monitor and control the Project Chimera agent swarm. It provides visibility into campaign progress, agent health, and financial status.

**SRS Reference**: §4.6 Orchestration, FR6.3 Telemetry
**Technology**: Streamlit (Python)

---

## 2. Functional Requirements

### UI1: Campaign Dashboard
**As a** Campaign Manager,
**I need** to create and monitor campaigns,
**So that** I can track progress against goals.

**Features**:
- **Create Campaign Form**: Input for Name, Goal, Budget, Audience, Platforms.
- **Campaign List**: Table showing active campaigns with progress bars (% tasks completed).
- **Detail View**: Drill-down to see specific tasks and their status (Pending, Running, Completed, Failed).

### UI2: Agent Monitor
**As a** System Operator,
**I need** to see the real-time status of all agents,
**So that** I can identify bottlenecks or failures.

**Features**:
- **Agent Grid**: Cards for each active agent (Planner, Worker, Judge).
- **Health Indicators**: Status (Idle/Busy/Offline), Last Heartbeat.
- **Current Activity**: What task is the agent working on right now?

### UI3: Financial Overview
**As a** Financial Controller,
**I need** to see wallet balances and transaction logs,
**So that** I can audit spending.

**Features**:
- **Total Spend**: Aggregate cost across all campaigns.
- **Wallet Balances**: Table of agent wallet balances.
- **Transaction Log**: List of recent transactions with receipt hashes.

---

## 3. Technical Architecture

### Stack
- **Framework**: Streamlit
- **Backend**: Direct imports of `src` modules (Planner, Orchestrator) or API calls if service-separated.
- **State Management**: Streamlit Session State.

### Directory Structure
```
src/frontend/
├── app.py              # Main entry point
├── components/         # Reusable UI widgets
│   ├── campaign_form.py
│   ├── agent_card.py
│   └── finance_chart.py
└── pages/              # Multi-page layout
    ├── 1_Campaigns.py
    ├── 2_Agents.py
    └── 3_Finance.py
```

---

## 4. Mockups (Textual)

**Home Page**
```
+--------------------------------------------------+
|  PROJECT CHIMERA COMMAND CENTER                  |
+--------------------------------------------------+
|  [Active Campaigns: 3]  [Agents Online: 5]       |
+--------------------------------------------------+
|  Recent Activity Log                             |
|  - [Worker-01] Published post to Twitter         |
|  - [Planner-01] Created tasks for Campaign A     |
+--------------------------------------------------+
```

**Campaign Creation**
```
+--------------------------------------------------+
|  Create New Campaign                             |
+--------------------------------------------------+
|  Name: [ Summer Launch ]                         |
|  Goal: [ Promote new product line... ]           |
|  Budget: [ $5000 ]                               |
|  [ Create Campaign ]                             |
+--------------------------------------------------+
```
