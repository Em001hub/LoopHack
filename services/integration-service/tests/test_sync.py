"""Tests for sync service functionality."""
import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.services.sync_service import SyncService
from src.models.unified import User, Project, Task


class TestSyncService:
    """Test sync service operations."""
    
    @pytest.fixture
    def mock_db(self):
        """Create a mock database session."""
        db = Mock()
        db.query = Mock()
        db.add = Mock()
        db.commit = Mock()
        db.rollback = Mock()
        return db
    
    @pytest.fixture
    def sync_service(self, mock_db):
        """Create a sync service instance."""
        return SyncService(mock_db)
    
    def test_upsert_user_creates_new(self, sync_service, mock_db):
        """Test upserting a new user."""
        user = User(
            id="test_user_1",
            email="test@example.com",
            name="Test User",
            source="jira",
            metadata={}
        )
        
        # Mock query to return None (user doesn't exist)
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        sync_service._upsert_user(user)
        
        assert mock_db.add.called
        assert sync_service.sync_stats["users"]["created"] == 1
    
    def test_upsert_user_updates_existing(self, sync_service, mock_db):
        """Test upserting an existing user."""
        user = User(
            id="test_user_1",
            email="updated@example.com",
            name="Updated User",
            source="jira",
            metadata={}
        )
        
        # Mock query to return existing user
        existing_user = Mock()
        mock_db.query.return_value.filter.return_value.first.return_value = existing_user
        
        sync_service._upsert_user(user)
        
        assert existing_user.email == "updated@example.com"
        assert existing_user.name == "Updated User"
        assert sync_service.sync_stats["users"]["updated"] == 1
    
    def test_upsert_project_creates_new(self, sync_service, mock_db):
        """Test upserting a new project."""
        project = Project(
            id="test_project_1",
            name="Test Project",
            key="PROJ",
            source="jira",
            url="https://example.com",
            metadata={}
        )
        
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        sync_service._upsert_project(project)
        
        assert mock_db.add.called
        assert sync_service.sync_stats["projects"]["created"] == 1
    
    def test_upsert_task_creates_new(self, sync_service, mock_db):
        """Test upserting a new task."""
        from datetime import datetime
        
        task = Task(
            id="test_task_1",
            project_id="test_project_1",
            title="Test Task",
            status="To Do",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            source="jira",
            metadata={}
        )
        
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        sync_service._upsert_task(task)
        
        assert mock_db.add.called
        assert sync_service.sync_stats["tasks"]["created"] == 1
    
    @pytest.mark.asyncio
    async def test_sync_all_success(self, sync_service):
        """Test successful full sync."""
        with patch.object(sync_service, 'sync_jira', new_callable=AsyncMock) as mock_jira, \
             patch.object(sync_service, 'sync_github', new_callable=AsyncMock) as mock_github, \
             patch.object(sync_service, 'sync_slack', new_callable=AsyncMock) as mock_slack, \
             patch.object(sync_service, 'sync_calendar', new_callable=AsyncMock) as mock_calendar:
            
            result = await sync_service.sync_all()
            
            assert result["status"] == "success"
            assert "duration_seconds" in result
            assert "stats" in result
            assert mock_jira.called
            assert mock_github.called
            assert mock_slack.called
            assert mock_calendar.called
    
    @pytest.mark.asyncio
    async def test_sync_all_handles_error(self, sync_service):
        """Test sync_all handles errors gracefully."""
        with patch.object(sync_service, 'sync_jira', new_callable=AsyncMock) as mock_jira:
            mock_jira.side_effect = Exception("Sync failed")
            
            result = await sync_service.sync_all()
            
            assert result["status"] == "error"
            assert "error" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
