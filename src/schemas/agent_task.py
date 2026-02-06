"""
Agent Task Schema Validation

SRS Reference: §3.1 fastRender Swarm
Spec: specs/technical.md, Agent Task Schema (lines 15-186)

This module provides validation logic for Agent Task Manifests and Results
using JSON Schema.
"""

import json
import os
from typing import Dict, Any, List, Optional
import jsonschema
from datetime import datetime

# Define the Task Manifest Schema directly from specs/technical.md
# In a real production system, we might load this from a .json file
TASK_MANIFEST_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "AgentTaskManifest",
    "type": "object",
    "required": [
        "task_id",
        "campaign_id",
        "task_type",
        "created_at",
        "planner_soul_id",
        "payload",
        "dependencies",
        "timeout_seconds",
        "priority"
    ],
    "properties": {
        "task_id": {
            "type": "string",
            # "format": "uuid", # Python jsonschema format validation requires extra deps
            "description": "Globally unique task identifier"
        },
        "campaign_id": {
            "type": "string",
            # "format": "uuid",
            "description": "Parent campaign identifier"
        },
        "task_type": {
            "type": "string",
            "enum": [
                "content_generation",
                "content_review",
                "social_publish",
                "analytics_fetch",
                "transaction_execute"
            ],
            "description": "Type of task to execute"
        },
        "created_at": {
            "type": "string",
            # "format": "date-time",
            "description": "ISO 8601 timestamp of task creation"
        },
        "planner_soul_id": {
            "type": "string",
            "description": "SOUL ID of the planner agent that created this task"
        },
        "payload": {
            "type": "object",
            "description": "Task-specific input data"
        },
        "dependencies": {
            "type": "array",
            "items": { "type": "string" }, # Simplified for uuid check
            "description": "List of task_ids that must complete before this task"
        },
        "timeout_seconds": {
            "type": "integer",
            "minimum": 1,
            "maximum": 3600,
            "description": "Maximum execution time before task is considered failed"
        },
        "priority": {
            "type": "string",
            "enum": ["HIGH", "NORMAL", "LOW"],
            "default": "NORMAL"
        }
    }
}

TASK_RESULT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "AgentTaskResult",
    "type": "object",
    "required": [
        "task_id",
        "worker_soul_id",
        "status",
        "completed_at",
        "confidence",
        "output"
    ],
    "properties": {
        "task_id": {
            "type": "string"
        },
        "worker_soul_id": {
            "type": "string",
            "description": "SOUL ID of the worker that executed this task"
        },
        "status": {
            "type": "string",
            "enum": ["SUCCESS", "FAILED", "ESCALATED"],
            "description": "Task execution outcome"
        },
        "completed_at": {
            "type": "string"
        },
        "confidence": {
            "type": "number",
            "minimum": 0.0,
            "maximum": 1.0,
            "description": "Worker's confidence in the result quality"
        },
        "output": {
            "type": "object",
            "description": "Task-specific output data"
        },
        "proof": {
            "type": "object",
            "description": "Evidence bundle for Judge review"
        },
        "error": {
            "type": "object"
        }
    }
}

def validate_task_manifest(manifest: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate an Agent Task Manifest against the schema.
    
    Args:
        manifest: Dictionary containing the task manifest data
        
    Returns:
        Dict with keys:
            - valid (bool): True if valid
            - errors (List[str]): List of error messages if invalid
    
    SRS Reference: §3.1 fastRender Swarm
    Spec: specs/technical.md, Task Manifest Schema
    """
    try:
        jsonschema.validate(instance=manifest, schema=TASK_MANIFEST_SCHEMA)
        return {"valid": True, "errors": []}
    except jsonschema.ValidationError as e:
        return {"valid": False, "errors": [e.message]}
    except Exception as e:
        return {"valid": False, "errors": [str(e)]}

def validate_task_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate an Agent Task Result against the schema.
    
    Args:
        result: Dictionary containing the task result data
        
    Returns:
        Dict with keys:
            - valid (bool): True if valid
            - errors (List[str]): List of error messages if invalid
            
    SRS Reference: §3.1 fastRender Swarm
    Spec: specs/technical.md, Task Result Schema
    """
    try:
        jsonschema.validate(instance=result, schema=TASK_RESULT_SCHEMA)
        return {"valid": True, "errors": []}
    except jsonschema.ValidationError as e:
        return {"valid": False, "errors": [e.message]}
    except Exception as e:
        return {"valid": False, "errors": [str(e)]}
