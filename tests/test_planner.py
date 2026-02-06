"""
Planner Service Tests

SRS Reference: §4.6 Orchestration (FR6.1, FR6.2)
Spec: specs/planner_service.md

These tests validate the campaign decomposition logic of the Planner Service.
"""

import pytest
import uuid
from datetime import datetime, timezone
from src.planner.engine import CampaignPlanner
from src.schemas.agent_task import validate_task_manifest

class TestCampaignPlanner:
    
    @pytest.fixture
    def valid_campaign_manifest(self):
        return {
            "campaign_id": str(uuid.uuid4()),
            "name": "Summer Launch",
            "goal": "Promote summer collection on Instagram",
            "budget_limit_usd": 1000.0,
            "start_date": datetime.now(timezone.utc).isoformat(),
            "end_date": datetime.now(timezone.utc).isoformat(),
            "target_audience": {
                "demographics": ["GenZ"],
                "regions": ["US"]
            },
            "constraints": {
                "platforms": ["instagram"]
            }
        }

    def test_plan_campaign_returns_valid_tasks(self, valid_campaign_manifest):
        """FR6.2: Planner must return a list of valid AgentTaskManifests."""
        planner = CampaignPlanner()
        tasks = planner.plan_campaign(valid_campaign_manifest)
        
        assert len(tasks) > 0, "Planner should return at least one task"
        
        for task in tasks:
            # Validate against our strict schema
            validation = validate_task_manifest(task)
            assert validation["valid"] is True, f"Invalid task generated: {validation['errors']}"
            
            # Check traceability
            assert task["campaign_id"] == valid_campaign_manifest["campaign_id"]
            assert task["planner_soul_id"] == "planner-001" # Mock ID

    def test_plan_campaign_creates_valid_dag(self, valid_campaign_manifest):
        """FR6.2: Tasks must form a valid dependency graph (Trend -> Content -> Publish)."""
        planner = CampaignPlanner()
        tasks = planner.plan_campaign(valid_campaign_manifest)
        
        # Sort by task type to verify flow
        task_types = [t["task_type"] for t in tasks]
        
        # Verify standard pattern presence
        assert "analytics_fetch" in task_types
        assert "content_generation" in task_types
        assert "social_publish" in task_types
        
        # Find specific tasks
        fetch_task = next(t for t in tasks if t["task_type"] == "analytics_fetch")
        gen_task = next(t for t in tasks if t["task_type"] == "content_generation")
        
        # Verify dependency: Generation depends on Fetch
        assert fetch_task["task_id"] in gen_task["dependencies"], "Content Gen must depend on Trends"

    def test_encodes_payload_correctly(self, valid_campaign_manifest):
        """FR2.2: Campaign context/constraints must be passed to task payloads."""
        planner = CampaignPlanner()
        tasks = planner.plan_campaign(valid_campaign_manifest)
        
        fetch_task = next(t for t in tasks if t["task_type"] == "analytics_fetch")
        
        # Verify constraint propagation
        assert fetch_task["payload"]["platform"] == "instagram"
        assert fetch_task["payload"]["region"] == "US" # inferred from target_audience

    def test_validates_budget_limit(self):
        """FR5.3: Planner should respect budget limits."""
        planner = CampaignPlanner()
        # To decide: Should planner raise error or just plan within budget?
        # For MVP, we presume valid input, but this is a placeholder for logic
        pass 
