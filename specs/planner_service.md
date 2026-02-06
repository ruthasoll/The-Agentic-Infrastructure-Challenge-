# Planner Service Specification

## 1. Overview
The **Planner Service** is the brain of the FastRender Swarm. It accepts high-level **Campaign Manifests** from the Campaign Manager (User) and decomposes them into a Directed Acyclic Graph (DAG) of atomic **Agent Task Manifests**.

**SRS Reference**: §4.6 Orchestration, FR6.1, FR6.2  
**Functional Reference**: FR2.2 (Campaign Context), FR4.1 (Workflow Execution)

---

## 2. Campaign Manifest Schema (Input)

The `CampaignManifest` represents the user's high-level goal.

```json
{
  "campaign_id": "uuid-string",
  "name": "Summer Collection Launch",
  "goal": "Increase brand awareness for new summer line by 20% in GenZ demographic",
  "budget_limit_usd": 5000.00,
  "start_date": "2023-06-01T00:00:00Z",
  "end_date": "2023-08-31T23:59:59Z",
  "target_audience": {
    "demographics": ["GenZ", "Millennials"],
    "interests": ["Fashion", "Sustainability", "Beach Life"],
    "regions": ["US", "EU"]
  },
  "constraints": {
    "prohibited_keywords": ["fast fashion", "cheap", "waste"],
    "brand_voice": "Eco-conscious, vibrant, youthful",
    "platforms": ["instagram", "tiktok"]
  }
}
```

### Key Fields
- **goal**: Natural language description of the objective. Used by the Planner LLM to infer tasks.
- **constraints**: Hard limits on content and execution.
- **budget_limit_usd**: Total budget cap for all child tasks combined.

---

## 3. Decomposition Logic

The Planner Engine uses a **ReAct-style** decomposition process (or a deterministic template for MVP) to break down the `goal`.

### Standard Workflow Patterns

#### Pattern A: Trend-Jacked Content (Standard)
1.  **Task 1 (Fetch Trends)**: `task_type="analytics_fetch"`
    -   *Input*: Platforms=["instagram", "tiktok"], Category="Fashion"
    -   *Output*: List of trending hashtags (e.g., #SummerVibes)
2.  **Task 2 (Generate Content)**: `task_type="content_generation"`
    -   *Dependency*: Task 1
    -   *Input*: Prompt="Create post about summer line using #SummerVibes", Context=Task1.Output
3.  **Task 3 (Review Content)**: `task_type="content_review"`
    -   *Dependency*: Task 2
    -   *Input*: Content=Task2.Output, Guidelines=Campaign.constraints
4.  **Task 4 (Publish)**: `task_type="social_publish"`
    -   *Dependency*: Task 3
    -   *Input*: Content=Task3.Output.ApprovedContent

---

## 4. Planner Output

The Planner produces a list of `AgentTaskManifest` objects (see `specs/technical.md` lines 15-100) that form a valid DAG.

### Validation Rules
1.  **DAG Integrity**: No circular dependencies in `dependencies` array.
2.  **Budget Check**: Sum of nested task budgets defined in `payload` (if applicable) must not exceed `campaign.budget_limit_usd`.
3.  **Traceability**: Every child task must reference `campaign_id`.

---

## 5. Interface Definition

```python
class CampaignPlanner:
    def plan_campaign(self, manifest: Dict[str, Any]) -> List[AgentTaskManifest]:
        """
        Decomposes a campaign into a list of executable tasks.
        
        Args:
            manifest: The CampaignManifest JSON dictionary.
            
        Returns:
            List of AgentTaskManifest dictionaries ready for the Task Queue.
            
        Raises:
            ValueError: If manifest is invalid or budget constrained.
        """
        pass
```
