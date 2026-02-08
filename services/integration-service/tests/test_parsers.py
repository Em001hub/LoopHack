"""Comprehensive tests for parser functions."""
import pytest
from src.integrations.jira.parser import parse_jira_project, parse_jira_issue
from src.integrations.github.parser import parse_github_repo, parse_github_commit, parse_github_pr
from src.integrations.slack.parser import parse_slack_channel, parse_slack_message, parse_slack_user


class TestJiraParser:
    """Test Jira data parsers."""
    
    def test_parse_jira_project(self):
        """Test parsing Jira project data."""
        raw_project = {
            "id": "10000",
            "key": "PROJ",
            "name": "Test Project",
            "description": "A test project"
        }
        
        project = parse_jira_project(raw_project)
        
        assert project.id == "jira_10000"
        assert project.key == "PROJ"
        assert project.name == "Test Project"
        assert project.source == "jira"
    
    def test_parse_jira_issue(self):
        """Test parsing Jira issue data."""
        raw_issue = {
            "id": "10001",
            "key": "PROJ-123",
            "fields": {
                "summary": "Test Issue",
                "status": {"name": "To Do"},
                "created": "2024-01-01T00:00:00.000Z",
                "updated": "2024-01-02T00:00:00.000Z"
            }
        }
        
        task = parse_jira_issue(raw_issue, "jira_10000")
        
        assert task.id == "jira_10001"
        assert task.title == "Test Issue"
        assert task.project_id == "jira_10000"
        assert task.status == "To Do"
        assert task.source == "jira"


class TestGitHubParser:
    """Test GitHub data parsers."""
    
    def test_parse_github_repo(self):
        """Test parsing GitHub repository data."""
        raw_repo = {
            "id": 123456,
            "name": "test-repo",
            "full_name": "owner/test-repo",
            "description": "A test repository",
            "html_url": "https://github.com/owner/test-repo"
        }
        
        project = parse_github_repo(raw_repo)
        
        assert project.id == "github_123456"
        assert project.name == "test-repo"
        assert project.key == "owner/test-repo"
        assert project.source == "github"
        assert project.url == "https://github.com/owner/test-repo"
    
    def test_parse_github_commit(self):
        """Test parsing GitHub commit data."""
        raw_commit = {
            "sha": "abc123",
            "commit": {
                "message": "Fix bug",
                "author": {
                    "name": "John Doe",
                    "date": "2024-01-01T00:00:00Z"
                }
            }
        }
        
        event = parse_github_commit(raw_commit, "owner/test-repo")
        
        assert event.id == "github_commit_abc123"
        assert event.event_type == "commit"
        assert event.source == "github"
    
    def test_parse_github_pr(self):
        """Test parsing GitHub pull request data."""
        raw_pr = {
            "id": 789,
            "number": 42,
            "title": "Add new feature",
            "state": "open",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-02T00:00:00Z"
        }
        
        task = parse_github_pr(raw_pr, "owner/test-repo")
        
        assert task.id == "github_pr_789"
        assert task.title == "Add new feature"
        assert task.status == "open"
        assert task.source == "github"


class TestSlackParser:
    """Test Slack data parsers."""
    
    def test_parse_slack_channel(self):
        """Test parsing Slack channel data."""
        raw_channel = {
            "id": "C123456",
            "name": "general",
            "is_channel": True,
            "topic": {"value": "General discussion"}
        }
        
        project = parse_slack_channel(raw_channel)
        
        assert project.id == "slack_C123456"
        assert project.name == "general"
        assert project.key == "general"
        assert project.source == "slack"
    
    def test_parse_slack_message(self):
        """Test parsing Slack message data."""
        raw_message = {
            "ts": "1234567890.123456",
            "user": "U123456",
            "text": "Hello, world!",
            "type": "message"
        }
        
        event = parse_slack_message(raw_message, "C123456")
        
        assert event.id == "slack_message_1234567890.123456"
        assert event.event_type == "message"
        assert event.source == "slack"
    
    def test_parse_slack_user(self):
        """Test parsing Slack user data."""
        raw_user = {
            "id": "U123456",
            "name": "johndoe",
            "real_name": "John Doe",
            "profile": {
                "email": "john@example.com"
            }
        }
        
        user = parse_slack_user(raw_user)
        
        assert user.id == "slack_U123456"
        assert user.name == "John Doe"
        assert user.email == "john@example.com"
        assert user.source == "slack"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
