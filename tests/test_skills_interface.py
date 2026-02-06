"""
Test Skills Interface Contracts

Spec Reference: skills/skill_fetch_trends/README.md
SRS Reference: §4.2 Perception (FR2.2), research/tooling_strategy.md

These tests validate that skill modules accept the correct input/output contracts
defined in their README specifications. Tests enforce the interface between
Workers and Skills via MCP Gateway.

Status: FAILING (skill modules don't exist yet, only README specs)
Next Step: Implement skills/skill_fetch_trends/skill.py with execute_skill()
"""

import pytest
from typing import Dict, Any


class TestSkillFetchTrendsInterface:
    """
    Test fetch_trends skill interface contract.
    
    Spec: skills/skill_fetch_trends/README.md
    Input Schema: lines 23-58
    Output Schema: lines 62-108
    """
    
    def test_fetch_trends_accepts_valid_input(self):
        """
        Test that fetch_trends skill accepts valid input matching the spec.
        
        Required fields: platform
        Optional fields: category, region, limit
        """
        valid_input = {
            "platform": "twitter",
            "category": "tech",
            "region": "US",
            "limit": 5
        }
        
        # This will fail because skill module doesn't exist yet
        from skills.skill_fetch_trends.skill import execute_skill
        
        # Should not raise an exception for valid input
        result = execute_skill(valid_input)
        
        # Result should have the expected structure
        assert "trends" in result
        assert "metadata" in result
        assert isinstance(result["trends"], list)
    
    def test_fetch_trends_validates_platform_enum(self):
        """
        Test that fetch_trends rejects invalid platform values.
        
        Spec: Valid platforms are twitter, instagram, tiktok, reddit
        """
        invalid_input = {
            "platform": "invalid_platform"
        }
        
        from skills.skill_fetch_trends.skill import execute_skill
        
        # Should raise validation error for invalid platform
        with pytest.raises(ValueError, match="platform"):
            execute_skill(invalid_input)
    
    def test_fetch_trends_returns_correct_output_structure(self):
        """
        Test that fetch_trends returns output matching the spec schema.
        
        Spec: Output must include trends[] array and metadata object
        Each trend must have: topic, volume, sentiment, retrieved_at
        """
        valid_input = {
            "platform": "twitter",
            "limit": 3
        }
        
        from skills.skill_fetch_trends.skill import execute_skill
        
        result = execute_skill(valid_input)
        
        # Validate output structure
        assert "trends" in result
        assert "metadata" in result
        
        # Validate trends array
        assert isinstance(result["trends"], list)
        assert len(result["trends"]) <= 3
        
        # Validate each trend has required fields
        for trend in result["trends"]:
            assert "topic" in trend
            assert "volume" in trend
            assert "sentiment" in trend
            assert "retrieved_at" in trend
            
            # Validate sentiment range (-1.0 to 1.0)
            assert -1.0 <= trend["sentiment"] <= 1.0
            
            # Validate volume is non-negative
            assert trend["volume"] >= 0


class TestSkillGenerateContentInterface:
    """
    Test generate_content skill interface contract.
    
    Spec: research/tooling_strategy.md, Skill 2
    SRS: §4.3 Creative Engine (FR3.1)
    """
    
    def test_generate_content_accepts_valid_input(self):
        """
        Test that generate_content skill accepts valid input.
        
        Required fields: soul_id, content_type, prompt
        Optional fields: context_ids, max_length
        """
        valid_input = {
            "soul_id": "chimera:agent:uuid-123",
            "content_type": "post",
            "prompt": "Create a post about AI trends in 2026",
            "context_ids": ["citation:uuid-456"],
            "max_length": 280
        }
        
        # This will fail because skill module doesn't exist yet
        from skills.skill_generate_content.skill import execute_skill
        
        result = execute_skill(valid_input)
        
        # Result should have the expected structure
        assert "content" in result
        assert "confidence" in result
        assert "citations" in result
        assert "model_metadata" in result
    
    def test_generate_content_validates_content_type(self):
        """
        Test that generate_content validates content_type enum.
        
        Spec: Valid types are post, image, video
        """
        invalid_input = {
            "soul_id": "chimera:agent:uuid-123",
            "content_type": "invalid_type",
            "prompt": "Test prompt"
        }
        
        from skills.skill_generate_content.skill import execute_skill
        
        with pytest.raises(ValueError, match="content_type"):
            execute_skill(invalid_input)
    
    def test_generate_content_returns_confidence_in_range(self):
        """
        Test that generate_content returns confidence between 0.0 and 1.0.
        
        Spec: confidence must be 0.0-1.0 for Judge evaluation
        """
        valid_input = {
            "soul_id": "chimera:agent:uuid-123",
            "content_type": "post",
            "prompt": "Test prompt"
        }
        
        from skills.skill_generate_content.skill import execute_skill
        
        result = execute_skill(valid_input)
        
        assert "confidence" in result
        assert 0.0 <= result["confidence"] <= 1.0


class TestSkillPublishPostInterface:
    """
    Test publish_post skill interface contract.
    
    Spec: research/tooling_strategy.md, Skill 3
    SRS: §4.4 Action System (FR4.2)
    """
    
    def test_publish_post_requires_provenance_metadata(self):
        """
        Test that publish_post requires provenance metadata bundle.
        
        Spec: provenance is required field with soul_id, confidence, etc.
        SRS: NFR ethical disclosure requirement
        """
        # Missing provenance should fail
        invalid_input = {
            "platform": "twitter",
            "content": "Test post"
            # Missing provenance (required)
        }
        
        from skills.skill_publish_post.skill import execute_skill
        
        with pytest.raises(ValueError, match="provenance"):
            execute_skill(invalid_input)
    
    def test_publish_post_returns_receipt_id(self):
        """
        Test that publish_post returns receipt_id for ledger tracking.
        
        Spec: Output must include receipt_id for transaction ledger
        SRS: §4.5 Commerce (FR5.2) - cryptographic receipts
        """
        valid_input = {
            "platform": "twitter",
            "content": "Test post",
            "provenance": {
                "soul_id": "chimera:agent:uuid-123",
                "confidence": 0.87,
                "human_override_flag": False,
                "trace_id": "trace_abc123:evt42"
            }
        }
        
        from skills.skill_publish_post.skill import execute_skill
        
        result = execute_skill(valid_input)
        
        assert "receipt_id" in result
        assert "post_id" in result
        assert "status" in result
        assert result["status"] in ["SUCCESS", "FAILED", "SCHEDULED"]


class TestSkillCheckWalletBalanceInterface:
    """
    Test check_wallet_balance skill interface contract.
    
    Spec: research/tooling_strategy.md, Skill 4
    SRS: §4.5 Commerce (FR5.1)
    """
    
    def test_check_wallet_balance_requires_soul_id(self):
        """
        Test that check_wallet_balance requires soul_id parameter.
        """
        invalid_input = {}  # Missing soul_id
        
        from skills.skill_check_wallet_balance.skill import execute_skill
        
        with pytest.raises(ValueError, match="soul_id"):
            execute_skill(invalid_input)
    
    def test_check_wallet_balance_returns_balance_and_currency(self):
        """
        Test that check_wallet_balance returns balance and currency.
        
        Spec: Output must include balance, currency, recent_transactions
        """
        valid_input = {
            "soul_id": "chimera:agent:uuid-123",
            "include_pending": True
        }
        
        from skills.skill_check_wallet_balance.skill import execute_skill
        
        result = execute_skill(valid_input)
        
        assert "balance" in result
        assert "currency" in result
        assert "recent_transactions" in result
        assert isinstance(result["balance"], (int, float))
        assert result["currency"] == "USD"


class TestSkillValidateImageInterface:
    """
    Test validate_image skill interface contract.
    
    Spec: research/tooling_strategy.md, Skill 5
    SRS: §4.3 Creative Engine (FR3.2)
    """
    
    def test_validate_image_requires_image_url_and_guidelines(self):
        """
        Test that validate_image requires image_url and brand_guidelines.
        """
        invalid_input = {
            "image_url": "https://s3.example.com/image123.png"
            # Missing brand_guidelines (required)
        }
        
        from skills.skill_validate_image.skill import execute_skill
        
        with pytest.raises(ValueError, match="brand_guidelines"):
            execute_skill(invalid_input)
    
    def test_validate_image_returns_validation_result_and_confidence(self):
        """
        Test that validate_image returns is_valid, confidence, and violations.
        
        Spec: Output must include is_valid (bool), confidence (0.0-1.0), violations[]
        """
        valid_input = {
            "image_url": "https://s3.example.com/image123.png",
            "brand_guidelines": {
                "allowed_colors": ["#FF5733", "#3498DB"],
                "prohibited_content": ["violence", "nudity"]
            }
        }
        
        from skills.skill_validate_image.skill import execute_skill
        
        result = execute_skill(valid_input)
        
        assert "is_valid" in result
        assert "confidence" in result
        assert "violations" in result
        assert isinstance(result["is_valid"], bool)
        assert 0.0 <= result["confidence"] <= 1.0
        assert isinstance(result["violations"], list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
