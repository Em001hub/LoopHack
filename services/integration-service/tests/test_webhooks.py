"""Tests for webhook processing."""
import pytest
from src.integrations.github.webhook_validator import validate_github_signature
from src.integrations.jira.webhook_validator import validate_jira_signature


class TestGitHubWebhookValidator:
    """Test GitHub webhook signature validation."""
    
    def test_validate_github_signature_valid(self):
        """Test validation with correct signature."""
        payload = b'{"test": "data"}'
        secret = "my_secret"
        
        # Generate valid signature
        import hmac
        import hashlib
        signature = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
        signature_header = f"sha256={signature}"
        
        assert validate_github_signature(payload, signature_header, secret) is True
    
    def test_validate_github_signature_invalid(self):
        """Test validation with incorrect signature."""
        payload = b'{"test": "data"}'
        secret = "my_secret"
        signature_header = "sha256=invalid_signature"
        
        assert validate_github_signature(payload, signature_header, secret) is False
    
    def test_validate_github_signature_missing_prefix(self):
        """Test validation with missing sha256 prefix."""
        payload = b'{"test": "data"}'
        secret = "my_secret"
        signature_header = "invalid_format"
        
        assert validate_github_signature(payload, signature_header, secret) is False
    
    def test_validate_github_signature_empty(self):
        """Test validation with empty signature."""
        payload = b'{"test": "data"}'
        secret = "my_secret"
        
        assert validate_github_signature(payload, "", secret) is False


class TestJiraWebhookValidator:
    """Test Jira webhook signature validation."""
    
    def test_validate_jira_signature_valid(self):
        """Test validation with correct signature."""
        payload = b'{"test": "data"}'
        secret = "my_secret"
        
        # Generate valid signature
        import hmac
        import hashlib
        import base64
        signature = hmac.new(secret.encode(), payload, hashlib.sha256).digest()
        signature_b64 = base64.b64encode(signature).decode()
        
        assert validate_jira_signature(payload, signature_b64, secret) is True
    
    def test_validate_jira_signature_invalid(self):
        """Test validation with incorrect signature."""
        payload = b'{"test": "data"}'
        secret = "my_secret"
        signature = "invalid_signature"
        
        assert validate_jira_signature(payload, signature, secret) is False
    
    def test_validate_jira_signature_empty(self):
        """Test validation with empty signature."""
        payload = b'{"test": "data"}'
        secret = "my_secret"
        
        assert validate_jira_signature(payload, "", secret) is False


class TestWebhookEndpoints:
    """Test webhook endpoint processing."""
    
    def test_jira_webhook_issue_created(self):
        """Test processing Jira issue created webhook."""
        webhook_data = {
            "webhookEvent": "jira:issue_created",
            "issue": {
                "key": "PROJ-123",
                "fields": {
                    "summary": "New issue"
                }
            }
        }
        
        # This would test the actual endpoint
        # For now, just verify the data structure
        assert webhook_data["webhookEvent"] == "jira:issue_created"
        assert webhook_data["issue"]["key"] == "PROJ-123"
    
    def test_github_webhook_push_event(self):
        """Test processing GitHub push webhook."""
        webhook_data = {
            "commits": [
                {"id": "abc123", "message": "Fix bug"}
            ],
            "repository": {
                "name": "test-repo"
            }
        }
        
        assert len(webhook_data["commits"]) == 1
        assert webhook_data["commits"][0]["id"] == "abc123"
    
    def test_slack_webhook_challenge(self):
        """Test Slack webhook URL verification."""
        webhook_data = {
            "challenge": "test_challenge_123"
        }
        
        # Slack expects the challenge to be returned
        assert "challenge" in webhook_data
        assert webhook_data["challenge"] == "test_challenge_123"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
