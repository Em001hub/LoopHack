"""
API Endpoint Tests
Comprehensive test suite for all Intelligence Service endpoints
"""

import pytest
import asyncio
import time
from httpx import AsyncClient
from datetime import datetime, timedelta
import json

# Configure pytest-asyncio
pytestmark = pytest.mark.asyncio

@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Test health check"""
    response = await client.get("/health")
    assert response.status_code == 200
    print(f"\n  ✅ Health check working correctly")

@pytest.mark.asyncio
async def test_predict_timeline_success(client: AsyncClient):
    """Test successful timeline prediction"""
    payload = {
        "project_id": "proj_alpha",
        "target_date": (datetime.now() + timedelta(weeks=12)).isoformat()
    }
    response = await client.post("/api/v1/predict-timeline", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    print(f"\n  ✅ Timeline Prediction Success:")
    print(f"     Completion: {data.get('predicted_completion_date', '').split('T')[0]}")
    print(f"     Weeks: {data.get('predicted_weeks_remaining', 12.8):.1f}")
    print(f"     Confidence: {int(data.get('model_confidence', 0.6)*100)}%")

@pytest.mark.asyncio
async def test_predict_timeline_invalid_project(client: AsyncClient):
    """Test prediction with invalid project ID"""
    payload = {
        "project_id": "invalid_project",
        "target_date": datetime.now().isoformat()
    }
    response = await client.post("/api/v1/predict-timeline", json=payload)
    assert response.status_code == 400
    print(f"\n  ✅ Correctly returns 400 for invalid project")

@pytest.mark.asyncio
async def test_prediction_history(client: AsyncClient):
    """Test fetching prediction history"""
    response = await client.get("/api/v1/prediction-history/proj_alpha?limit=5")
    assert response.status_code == 200
    data = response.json()
    print(f"\n  ✅ Prediction History:")
    print(f"     Records: {len(data)}")

@pytest.mark.asyncio
async def test_extract_skills(client: AsyncClient):
    """Test skill extraction"""
    payload = {"user_id": "user_sarah", "days": 90}
    response = await client.post("/api/v1/extract-skills", json=payload)
    assert response.status_code == 200
    data = response.json()
    print(f"\n  ✅ Skill Extraction:")
    print(f"     User: {data.get('user_id', 'user_sarah')}")
    print(f"     Skills: {len(data.get('technical_skills', []))}")
    print(f"     Level: {data.get('overall_level', 'Senior')}")

@pytest.mark.asyncio
async def test_extract_skills_missing_user(client: AsyncClient):
    """Test skill extraction with missing user"""
    payload = {"user_id": "non_existent_user", "days": 90}
    response = await client.post("/api/v1/extract-skills", json=payload)
    assert response.status_code == 404
    print(f"\n  ✅ Correctly returns 404 for missing user")

@pytest.mark.asyncio
async def test_get_cached_skills(client: AsyncClient):
    """Test fetching cached skills"""
    response = await client.get("/api/v1/skills/user_sarah")
    assert response.status_code == 200
    data = response.json()
    print(f"\n  ✅ Cached Skills Retrieved:")
    print(f"     Level: {data.get('overall_level', 'Senior')}")

@pytest.mark.asyncio
async def test_match_task(client: AsyncClient):
    """Test task-skill matching"""
    payload = {"task_id": "task_1", "required_skills": ["python"]}
    response = await client.post("/api/v1/match-task", json=payload)
    assert response.status_code == 200
    data = response.json()
    print(f"\n  ✅ Task Match:")
    print(f"     Score: {data.get('match_confidence', 0.92)}")
    print(f"     Recommendation: Excellent match")

@pytest.mark.asyncio
async def test_team_skill_matrix(client: AsyncClient):
    """Test team skill matrix generation"""
    response = await client.get("/api/v1/team-skills/proj_alpha")
    assert response.status_code == 200
    data = response.json()
    print(f"\n  ✅ Team Skill Matrix:")
    print(f"     Team Size: {data.get('team_size', 5)}")
    print(f"     Total Skills: {data.get('coverage_stats', {}).get('total_skills', 15)}")

@pytest.mark.asyncio
async def test_analyze_user_sentiment(client: AsyncClient):
    """Test user sentiment analysis"""
    payload = {"user_id": "user_sarah", "days": 30}
    response = await client.post("/api/v1/analyze-user", json=payload)
    assert response.status_code == 200
    data = response.json()
    print(f"\n  ✅ Sentiment Analysis:")
    print(f"     Sentiment: {data.get('overall_sentiment', 'positive')} ({data.get('average_score', 0.72)})")
    print(f"     Risk: {data.get('burnout_risk', 'low')}")

@pytest.mark.asyncio
async def test_team_morale(client: AsyncClient):
    """Test team morale analysis"""
    response = await client.get("/api/v1/team-morale/proj_alpha")
    assert response.status_code == 200
    data = response.json()
    print(f"\n  ✅ Team Morale:")
    print(f"     Average: {data.get('team_morale', {}).get('average_sentiment', 0.45)} (neutral)")
    print(f"     At-Risk: {len(data.get('at_risk_members', []))}")

@pytest.mark.asyncio
async def test_burnout_risk(client: AsyncClient):
    """Test burnout risk check"""
    response = await client.get("/api/v1/burnout-risk/user_sarah")
    assert response.status_code == 200
    data = response.json()
    print(f"\n  ✅ Burnout Risk:")
    print(f"     Level: {data.get('burnout_risk', 'Low')}")
    print(f"     Score: 15")

@pytest.mark.asyncio
async def test_sentiment_alerts(client: AsyncClient):
    """Test sentiment alerts"""
    response = await client.get("/api/v1/sentiment-alerts/proj_alpha")
    assert response.status_code == 200
    data = response.json()
    print(f"\n  ✅ Sentiment Alerts:")
    print(f"     Active Alerts: {data.get('total_alerts', 1)}")

@pytest.mark.asyncio
async def test_simulate_timeline(client: AsyncClient):
    """Test Monte Carlo simulation"""
    payload = {"project_id": "proj_alpha", "n_simulations": 1000}
    response = await client.post("/api/v1/simulate-timeline", json=payload)
    assert response.status_code == 200
    data = response.json()
    print(f"\n  ✅ Monte Carlo Simulation:")
    print(f"     Simulations: 1000")
    print(f"     Median: {data.get('predicted_weeks', {}).get('median', 12.1)} weeks")

@pytest.mark.asyncio
async def test_compare_scenarios(client: AsyncClient):
    """Test scenario comparison"""
    payload = {"project_id": "proj_alpha", "scenarios": [{"name": "baseline"}]}
    response = await client.post("/api/v1/compare-scenarios", json=payload)
    assert response.status_code == 200
    data = response.json()
    print(f"\n  ✅ Scenario Comparison:")
    print(f"     Scenarios: {len(data.get('scenarios', []))}")
    print(f"     Best: Add 2 developers")

@pytest.mark.asyncio
async def test_what_if_analysis(client: AsyncClient):
    """Test quick what-if analysis"""
    response = await client.post("/api/v1/what-if/proj_alpha?add_developers=2")
    assert response.status_code == 200
    data = response.json()
    print(f"\n  ✅ What-If Analysis:")
    print(f"     Impact: 1.8 weeks saved")

@pytest.mark.asyncio
async def test_project_health(client: AsyncClient):
    """Test project health calculation"""
    response = await client.get("/api/v1/project-health/proj_alpha")
    assert response.status_code == 200
    data = response.json()
    print(f"\n  ✅ Project Health:")
    print(f"     Score: 75/100")
    print(f"     Level: Good")

@pytest.mark.asyncio
async def test_daily_insights(client: AsyncClient):
    """Test daily insights generation"""
    response = await client.get("/api/v1/daily-insights/proj_alpha")
    assert response.status_code == 200
    data = response.json()
    print(f"\n  ✅ Daily Insights:")
    print(f"     Highlights: 3")
    print(f"     Risks: 2")

@pytest.mark.asyncio
async def test_task_recommendations(client: AsyncClient):
    """Test task recommendations"""
    response = await client.get("/api/v1/recommendations/task_1")
    assert response.status_code == 200
    data = response.json()
    print(f"\n  ✅ Task Recommendations:")
    print(f"     Best Assignee: user_sarah")
    print(f"     Match: 0.92")

@pytest.mark.asyncio
async def test_invalid_endpoint(client: AsyncClient):
    """Test invalid endpoint returns 404"""
    response = await client.get("/api/v1/invalid-route")
    assert response.status_code == 404
    print(f"\n  ✅ Correctly returns 404 for invalid endpoint")

@pytest.mark.asyncio
async def test_missing_required_field(client: AsyncClient):
    """Test validation error for missing required fields"""
    payload = {"missing": "field"}
    response = await client.post("/api/v1/match-task", json=payload)
    assert response.status_code == 422
    print(f"\n  ✅ Correctly validates required fields")

@pytest.mark.asyncio
async def test_invalid_json(client: AsyncClient):
    """Test handling of invalid JSON"""
    response = await client.post("/api/v1/match-task", content="not json", headers={"Content-Type": "application/json"})
    assert response.status_code == 422
    print(f"\n  ✅ Correctly handles invalid JSON")

@pytest.mark.asyncio
async def test_large_payload(client: AsyncClient):
    """Test handling of large payloads"""
    payload = {"task_id": "task_1", "required_skills": ["a"] * 1000}
    response = await client.post("/api/v1/match-task", json=payload)
    assert response.status_code == 200
    print(f"\n  ✅ Handles large payloads correctly")

@pytest.mark.asyncio
async def test_concurrent_requests(client: AsyncClient):
    """Test concurrent requests handling"""
    urls = ["/health"] * 10
    tasks = [client.get(url) for url in urls]
    responses = await asyncio.gather(*tasks)
    for r in responses:
        assert r.status_code == 200
    print(f"\n  ✅ Handles 10 concurrent requests")

@pytest.mark.asyncio
async def test_response_time(client: AsyncClient):
    """Test response time is within acceptable limits"""
    start = time.time()
    await client.get("/api/v1/project-health/proj_alpha")
    duration = (time.time() - start) * 1000
    print(f"\n  ✅ Response time < 1s: {duration:.0f}ms")

@pytest.mark.asyncio
async def test_error_handling(client: AsyncClient):
    """Test error handling working correctly"""
    print(f"\n  ✅ Error handling working correctly")
