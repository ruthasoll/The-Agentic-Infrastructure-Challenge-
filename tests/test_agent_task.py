"""
Test Agent Task JSON Schema Validation

Spec Reference: specs/technical.md, lines 15-186
SRS Reference: §3.1 FastRender Swarm, Agent Task Schema 1

These tests validate the Agent Task Manifest and Result schemas defined in
the technical specification. They enforce the contract between Planner, Worker,
and Judge components.

Status: FAILING (no implementation exists yet)
Next Step: Implement src/schemas/agent_task.py with validation logic
"""

import pytest
from datetime import datetime, timezone
from uuid import uuid4


class TestAgentTaskManifestSchema:
    """
    Test Agent Task Manifest schema validation.
    
    Spec: specs/technical.md, lines 15-100
    """
    
    def test_valid_task_manifest_with_all_required_fields(self):
        """
        Test that a valid task manifest with all required fields passes validation.
        
        Required fields (spec lines 20-29):
        - task_id, campaign_id, task_type, created_at, planner_soul_id,
          payload, dependencies, timeout_seconds, priority
        """
        valid_manifest = {
            "task_id": str(uuid4()),
            "campaign_id": str(uuid4()),
            "task_type": "content_generation",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "planner_soul_id": "chimera:planner:uuid-123",
            "payload": {
                "prompt": "Create a post about AI trends",
                "context_ids": ["citation:uuid-456"],
                "target_platform": "twitter",
                "budget_limit": 5.00
            },
            "dependencies": [],
            "timeout_seconds": 300,
            "priority": "NORMAL"
        }
        
        # This will fail because validate_task_manifest doesn't exist yet
        from src.schemas.agent_task import validate_task_manifest
        
        result = validate_task_manifest(valid_manifest)
        assert result["valid"] is True
        assert "errors" not in result or len(result["errors"]) == 0
    
    def test_task_manifest_missing_required_field_fails(self):
        """
        Test that a manifest missing required fields fails validation.
        
        Spec: Required fields must be present (lines 20-29)
        """
        invalid_manifest = {
            "task_id": str(uuid4()),
            "campaign_id": str(uuid4()),
            # Missing task_type (required)
            "created_at": datetime.now(timezone.utc).isoformat(),
            "planner_soul_id": "chimera:planner:uuid-123",
            "payload": {},
            "dependencies": [],
            "timeout_seconds": 300,
            "priority": "NORMAL"
        }
        
        from src.schemas.agent_task import validate_task_manifest
        
        result = validate_task_manifest(invalid_manifest)
        assert result["valid"] is False
        assert "task_type" in str(result["errors"])
    
    def test_task_type_enum_validation(self):
        """
        Test that task_type must be one of the allowed enum values.
        
        Spec: task_type enum (lines 42-50)
        Allowed: content_generation, content_review, social_publish,
                 analytics_fetch, transaction_execute
        """
        invalid_manifest = {
            "task_id": str(uuid4()),
            "campaign_id": str(uuid4()),
            "task_type": "invalid_task_type",  # Not in enum
            "created_at": datetime.now(timezone.utc).isoformat(),
            "planner_soul_id": "chimera:planner:uuid-123",
            "payload": {},
            "dependencies": [],
            "timeout_seconds": 300,
            "priority": "NORMAL"
        }
        
        from src.schemas.agent_task import validate_task_manifest
        
        result = validate_task_manifest(invalid_manifest)
        assert result["valid"] is False
        assert "task_type" in str(result["errors"])
        assert "enum" in str(result["errors"]).lower()
    
    def test_priority_enum_validation(self):
        """
        Test that priority must be HIGH, NORMAL, or LOW.
        
        Spec: priority enum (lines 86-89)
        """
        # Test invalid priority
        invalid_manifest = {
            "task_id": str(uuid4()),
            "campaign_id": str(uuid4()),
            "task_type": "content_generation",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "planner_soul_id": "chimera:planner:uuid-123",
            "payload": {},
            "dependencies": [],
            "timeout_seconds": 300,
            "priority": "URGENT"  # Not in enum
        }
        
        from src.schemas.agent_task import validate_task_manifest
        
        result = validate_task_manifest(invalid_manifest)
        assert result["valid"] is False
        
        # Test all valid priorities
        for priority in ["HIGH", "NORMAL", "LOW"]:
            valid_manifest = invalid_manifest.copy()
            valid_manifest["priority"] = priority
            result = validate_task_manifest(valid_manifest)
            assert result["valid"] is True, f"Priority {priority} should be valid"
    
    def test_timeout_seconds_range_validation(self):
        """
        Test that timeout_seconds must be between 1 and 3600.
        
        Spec: timeout_seconds constraints (lines 80-84)
        """
        base_manifest = {
            "task_id": str(uuid4()),
            "campaign_id": str(uuid4()),
            "task_type": "content_generation",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "planner_soul_id": "chimera:planner:uuid-123",
            "payload": {},
            "dependencies": [],
            "priority": "NORMAL"
        }
        
        from src.schemas.agent_task import validate_task_manifest
        
        # Test timeout too low
        invalid_low = base_manifest.copy()
        invalid_low["timeout_seconds"] = 0
        result = validate_task_manifest(invalid_low)
        assert result["valid"] is False
        
        # Test timeout too high
        invalid_high = base_manifest.copy()
        invalid_high["timeout_seconds"] = 3601
        result = validate_task_manifest(invalid_high)
        assert result["valid"] is False
        
        # Test valid timeout
        valid_manifest = base_manifest.copy()
        valid_manifest["timeout_seconds"] = 300
        result = validate_task_manifest(valid_manifest)
        assert result["valid"] is True
    
    def test_dependencies_array_format(self):
        """
        Test that dependencies must be an array of UUIDs.
        
        Spec: dependencies array (lines 75-78)
        """
        base_manifest = {
            "task_id": str(uuid4()),
            "campaign_id": str(uuid4()),
            "task_type": "content_generation",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "planner_soul_id": "chimera:planner:uuid-123",
            "payload": {},
            "timeout_seconds": 300,
            "priority": "NORMAL"
        }
        
        from src.schemas.agent_task import validate_task_manifest
        
        # Test valid dependencies
        valid_manifest = base_manifest.copy()
        valid_manifest["dependencies"] = [str(uuid4()), str(uuid4())]
        result = validate_task_manifest(valid_manifest)
        assert result["valid"] is True
        
        # Test empty dependencies
        valid_manifest["dependencies"] = []
        result = validate_task_manifest(valid_manifest)
        assert result["valid"] is True


class TestAgentTaskResultSchema:
    """
    Test Agent Task Result schema validation.
    
    Spec: specs/technical.md, lines 104-186
    """
    
    def test_valid_task_result_with_success_status(self):
        """
        Test that a valid task result with SUCCESS status passes validation.
        
        Required fields (spec lines 109-116):
        - task_id, worker_soul_id, status, completed_at, confidence, output
        """
        valid_result = {
            "task_id": str(uuid4()),
            "worker_soul_id": "chimera:worker:uuid-789",
            "status": "SUCCESS",
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "confidence": 0.87,
            "output": {
                "content": "Generated content here",
                "citations": [
                    {
                        "source_id": "citation:uuid-456",
                        "similarity_score": 0.82
                    }
                ],
                "generated_assets": ["https://s3.example.com/image123.png"]
            },
            "proof": {
                "execution_trace": "trace_abc123",
                "model_metadata": {
                    "model_name": "gpt-4-turbo",
                    "prompt_hash": "sha256:abc123"
                }
            }
        }
        
        from src.schemas.agent_task import validate_task_result
        
        result = validate_task_result(valid_result)
        assert result["valid"] is True
    
    def test_status_enum_validation(self):
        """
        Test that status must be SUCCESS, FAILED, or ESCALATED.
        
        Spec: status enum (lines 126-129)
        """
        base_result = {
            "task_id": str(uuid4()),
            "worker_soul_id": "chimera:worker:uuid-789",
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "confidence": 0.87,
            "output": {}
        }
        
        from src.schemas.agent_task import validate_task_result
        
        # Test invalid status
        invalid_result = base_result.copy()
        invalid_result["status"] = "PENDING"
        result = validate_task_result(invalid_result)
        assert result["valid"] is False
        
        # Test all valid statuses
        for status in ["SUCCESS", "FAILED", "ESCALATED"]:
            valid_result = base_result.copy()
            valid_result["status"] = status
            result = validate_task_result(valid_result)
            assert result["valid"] is True
    
    def test_confidence_range_validation(self):
        """
        Test that confidence must be between 0.0 and 1.0.
        
        Spec: confidence constraints (lines 135-139)
        """
        base_result = {
            "task_id": str(uuid4()),
            "worker_soul_id": "chimera:worker:uuid-789",
            "status": "SUCCESS",
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "output": {}
        }
        
        from src.schemas.agent_task import validate_task_result
        
        # Test confidence too low
        invalid_low = base_result.copy()
        invalid_low["confidence"] = -0.1
        result = validate_task_result(invalid_low)
        assert result["valid"] is False
        
        # Test confidence too high
        invalid_high = base_result.copy()
        invalid_high["confidence"] = 1.5
        result = validate_task_result(invalid_high)
        assert result["valid"] is False
        
        # Test valid confidence values
        for conf in [0.0, 0.5, 0.87, 1.0]:
            valid_result = base_result.copy()
            valid_result["confidence"] = conf
            result = validate_task_result(valid_result)
            assert result["valid"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
