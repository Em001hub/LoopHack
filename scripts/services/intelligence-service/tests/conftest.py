"""Test configuration and fixtures"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def sample_project_data():
    """Sample project data for testing"""
    return {
        'remaining_story_points': 100,
        'avg_weekly_velocity': 20,
        'velocity_std': 3,
        'team_size': 5,
        'blocked_tasks_count': 2,
        'high_complexity_count': 5,
        'avg_task_age_days': 7,
        'team_experience_score': 0.75
    }
@pytest.fixture
async def client():
    """Create test client"""
    from httpx import AsyncClient
    from src.main import app
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
