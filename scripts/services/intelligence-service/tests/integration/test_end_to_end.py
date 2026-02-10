"""
Integration Tests
End-to-end testing of complete workflows
"""

import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta
from loguru import logger
import os
import sys
import asyncio

# Ensure pytest-asyncio is used
pytest_plugins = ["pytest_asyncio"]

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


class TestEndToEndPredictionFlow:
    """Test complete prediction workflow"""
    
    @pytest.mark.asyncio
    async def test_complete_prediction_flow(self, client: AsyncClient):
        """
        Test full prediction flow:
        1. Request prediction
        2. Store in database
        3. Retrieve history
        4. Trigger recalculation
        """
        print("\n" + "="*60)
        print("🔄 Testing Complete Prediction Flow")
        print("="*60)
        
        project_id = "proj_integration_test"
        
        # Step 1: Request prediction
        print("\n📊 Step 1: Requesting timeline prediction...")
        prediction_payload = {
            "project_id": project_id,
            "target_date": "2024-04-01T00:00:00Z"
        }
        
        response = await client.post("/api/v1/predict-timeline", json=prediction_payload)
        assert response.status_code == 200
        prediction = response.json()
        
        print(f"✅ Prediction received:")
        print(f"   Completion: {prediction['predicted_completion_date']}")
        print(f"   Weeks: {prediction['predicted_weeks_remaining']:.1f}")
        print(f"   Probability on time: {prediction.get('probability_on_time', 'N/A')}")
        
        # Step 2: Verify prediction was stored
        print("\n📜 Step 2: Checking prediction history...")
        await asyncio.sleep(0.5)  # Allow time for storage
        
        response = await client.get(f"/api/v1/prediction-history/{project_id}")
        assert response.status_code == 200
        history = response.json()
        
        print(f"✅ Found {len(history)} historical predictions")
        
        # Step 3: Trigger recalculation
        print("\n🔄 Step 3: Triggering background recalculation...")
        response = await client.post(f"/api/v1/recalculate-timeline/{project_id}")
        assert response.status_code == 200
        result = response.json()
        
        print(f"✅ Recalculation {result['status']}")
        
        print("\n" + "="*60)
        print("✅ PREDICTION FLOW TEST PASSED")
        print("="*60)


class TestEndToEndSkillFlow:
    """Test complete skill extraction workflow"""
    
    @pytest.mark.asyncio
    async def test_complete_skill_flow(self, client: AsyncClient):
        """
        Test full skill flow:
        1. Extract skills
        2. Cache skills
        3. Retrieve cached skills
        4. Match task
        5. Generate team matrix
        """
        print("\n" + "="*60)
        print("🔄 Testing Complete Skill Flow")
        print("="*60)
        
        user_id = "user_integration_test"
        
        # Step 1: Extract skills
        print("\n🔍 Step 1: Extracting user skills...")
        extract_payload = {
            "user_id": user_id,
            "days": 90
        }
        
        response = await client.post("/api/v1/extract-skills", json=extract_payload)
        assert response.status_code == 200
        skills = response.json()
        
        print(f"✅ Skills extracted:")
        print(f"   Technical skills: {len(skills['technical_skills'])}")
        print(f"   Overall level: {skills['overall_level']}")
        print(f"   Confidence: {skills['confidence']:.0%}")
        
        # Step 2: Retrieve cached skills
        print("\n📖 Step 2: Retrieving cached skills...")
        await asyncio.sleep(0.5)
        
        response = await client.get(f"/api/v1/skills/{user_id}")
        # May be 200 or 404 depending on caching
        if response.status_code == 200:
            cached_skills = response.json()
            print(f"✅ Found cached skills for {cached_skills['user_id']}")
        else:
            print(f"⚠️ No cached skills yet (expected in test environment)")
        
        # Step 3: Test task matching
        print("\n🎯 Step 3: Testing task matching...")
        match_payload = {
            "user_id": user_id,
            "task_id": "TEST-123",
            "task_requirements": {
                "required_skills": ["python", "javascript"],
                "preferred_skills": ["react", "docker"]
            }
        }
        
        response = await client.post("/api/v1/match-task", json=match_payload)
        assert response.status_code == 200
        match = response.json()
        
        print(f"✅ Task match:")
        print(f"   Score: {match['match_score']:.0%}")
        print(f"   Recommendation: {match['recommendation']}")
        
        # Step 4: Generate team matrix
        print("\n👥 Step 4: Generating team skill matrix...")
        response = await client.get("/api/v1/team-skills/proj_alpha")
        assert response.status_code == 200
        matrix = response.json()
        
        print(f"✅ Team skill matrix:")
        print(f"   Team size: {matrix['team_size']}")
        print(f"   Total skills: {matrix['coverage_stats']['total_skills']}")
        print(f"   Coverage: {matrix['coverage_stats']['coverage_score']:.0%}")
        
        print("\n" + "="*60)
        print("✅ SKILL FLOW TEST PASSED")
        print("="*60)


class TestEndToEndSentimentFlow:
    """Test complete sentiment analysis workflow"""
    
    @pytest.mark.asyncio
    async def test_complete_sentiment_flow(self, client: AsyncClient):
        """
        Test full sentiment flow:
        1. Analyze user sentiment
        2. Check burnout risk
        3. Analyze team morale
        4. Get sentiment alerts
        """
        print("\n" + "="*60)
        print("🔄 Testing Complete Sentiment Flow")
        print("="*60)
        
        user_id = "user_sarah"
        project_id = "proj_alpha"
        
        # Step 1: Analyze user sentiment
        print("\n😊 Step 1: Analyzing user sentiment...")
        sentiment_payload = {
            "user_id": user_id,
            "days": 30
        }
        
        response = await client.post("/api/v1/analyze-user", json=sentiment_payload)
        assert response.status_code == 200
        sentiment = response.json()
        
        if sentiment.get("status") == "insufficient_data":
            print(f"⚠️ Insufficient data (expected in test environment)")
        else:
            print(f"✅ Sentiment analyzed:")
            print(f"   Label: {sentiment['current_sentiment']['label']}")
            print(f"   Trend: {sentiment['sentiment_trend']['direction']}")
            print(f"   Burnout risk: {sentiment['burnout_risk']['level']}")
        
        # Step 2: Check burnout risk
        print("\n⚠️ Step 2: Checking burnout risk...")
        response = await client.get(f"/api/v1/burnout-risk/{user_id}")
        assert response.status_code == 200
        burnout = response.json()
        
        if "level" in burnout:
            print(f"✅ Burnout risk: {burnout['level']} (score: {burnout['score']})")
        else:
            print(f"⚠️ {burnout.get('recommended_action', 'No data')}")
        
        # Step 3: Analyze team morale
        print("\n👥 Step 3: Analyzing team morale...")
        response = await client.get(f"/api/v1/team-morale/{project_id}")
        assert response.status_code == 200
        morale = response.json()
        
        print(f"✅ Team morale:")
        print(f"   Overall: {morale['team_morale']['label']}")
        print(f"   Average: {morale['team_morale']['average_sentiment']:.2f}")
        print(f"   At risk: {len(morale['at_risk_members'])}")
        
        # Step 4: Get sentiment alerts
        print("\n🚨 Step 4: Fetching sentiment alerts...")
        response = await client.get(f"/api/v1/sentiment-alerts/{project_id}")
        assert response.status_code == 200
        alerts = response.json()
        
        print(f"✅ Active alerts: {alerts['alert_count']}")
        for alert in alerts['alerts'][:3]:
            print(f"   - {alert['severity']}: {alert['message']}")
        
        print("\n" + "="*60)
        print("✅ SENTIMENT FLOW TEST PASSED")
        print("="*60)


class TestEndToEndInsightFlow:
    """Test complete insight generation workflow"""
    
    @pytest.mark.asyncio
    async def test_complete_insight_flow(self, client: AsyncClient):
        """
        Test full insight flow:
        1. Run predictions
        2. Analyze sentiment
        3. Generate daily insights
        4. Get task recommendations
        5. Check project health
        """
        print("\n" + "="*60)
        print("🔄 Testing Complete Insight Flow")
        print("="*60)
        
        project_id = "proj_alpha"
        task_id = "PROJ-123"
        
        # Step 1: Get project health
        print("\n💚 Step 1: Checking project health...")
        response = await client.get(f"/api/v1/project-health/{project_id}")
        assert response.status_code == 200
        health = response.json()
        
        print(f"✅ Project health:")
        print(f"   Score: {health['overall_score']}/100")
        print(f"   Level: {health['health_level']}")
        
        # Step 2: Generate daily insights
        print("\n💡 Step 2: Generating daily insights...")
        response = await client.get(f"/api/v1/daily-insights/{project_id}")
        assert response.status_code == 200
        insights = response.json()
        
        print(f"✅ Daily insights generated:")
        print(f"   Summary: {insights['summary']}")
        print(f"   Highlights: {len(insights['highlights'])}")
        print(f"   Risks: {len(insights['risks'])}")
        
        for highlight in insights['highlights'][:3]:
            print(f"      {highlight}")
        
        # Step 3: Get task recommendations
        print("\n🎯 Step 3: Getting task recommendations...")
        response = await client.get(f"/api/v1/recommendations/{task_id}")
        assert response.status_code == 200
        recommendations = response.json()
        
        print(f"✅ Task recommendations:")
        print(f"   Best assignee: {recommendations['assignment']['recommended_assignee']}")
        print(f"   Match score: {recommendations['assignment']['match_score']:.0%}")
        print(f"   Est. hours: {recommendations['complexity']['estimated_hours']}")
        
        # Step 4: Run simulation
        print("\n🎲 Step 4: Running Monte Carlo simulation...")
        sim_payload = {
            "project_id": project_id,
            "n_simulations": 100
        }
        
        response = await client.post("/api/v1/simulate-timeline", json=sim_payload)
        assert response.status_code == 200
        simulation = response.json()
        
        print(f"✅ Simulation complete:")
        print(f"   Median: {simulation['predicted_weeks']['median']:.1f} weeks")
        print(f"   P90: {simulation['percentiles']['p90']:.1f} weeks")
        
        print("\n" + "="*60)
        print("✅ INSIGHT FLOW TEST PASSED")
        print("="*60)


class TestMultiServiceIntegration:
    """Test integration between multiple services"""
    
    @pytest.mark.asyncio
    async def test_cross_service_workflow(self, client: AsyncClient):
        """
        Test workflow that uses multiple services:
        1. Extract skills
        2. Analyze sentiment
        3. Make predictions
        4. Generate comprehensive insights
        """
        print("\n" + "="*60)
        print("🔄 Testing Cross-Service Integration")
        print("="*60)
        
        project_id = "proj_alpha"
        user_id = "user_sarah"
        
        print("\n🎯 Running parallel analysis...")
        
        # Run multiple analyses in parallel
        tasks = [
            client.post("/api/v1/extract-skills", json={"user_id": user_id, "days": 90}),
            client.post("/api/v1/analyze-user", json={"user_id": user_id, "days": 30}),
            client.post("/api/v1/predict-timeline", json={"project_id": project_id}),
            client.get(f"/api/v1/team-morale/{project_id}"),
        ]
        
        responses = await asyncio.gather(*tasks)
        
        # Verify all succeeded
        for i, response in enumerate(responses):
            assert response.status_code == 200
            print(f"✅ Task {i+1} completed successfully")
        
        # Now generate comprehensive insights using all data
        print("\n💡 Generating comprehensive insights...")
        response = await client.get(f"/api/v1/daily-insights/{project_id}")
        assert response.status_code == 200
        insights = response.json()
        
        print(f"\n✅ Comprehensive insights generated:")
        print(f"   {insights['summary']}")
        
        print("\n" + "="*60)
        print("✅ CROSS-SERVICE INTEGRATION TEST PASSED")
        print("="*60)


# Test fixtures

# Test fixtures moved to conftest.py


# Performance tests

class TestPerformance:
    """Test API performance"""
    
    @pytest.mark.asyncio
    async def test_prediction_performance(self, client: AsyncClient):
        """Test prediction endpoint performance"""
        import time
        
        print("\n" + "="*60)
        print("⚡ Testing Prediction Performance")
        print("="*60)
        
        payload = {"project_id": "proj_alpha"}
        
        start_time = time.time()
        response = await client.post("/api/v1/predict-timeline", json=payload)
        end_time = time.time()
        
        assert response.status_code == 200
        
        elapsed = (end_time - start_time) * 1000  # Convert to ms
        print(f"\n✅ Prediction completed in {elapsed:.0f}ms")
        
        # Should complete within reasonable time
        assert elapsed < 5000, "Prediction took too long"
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self, client: AsyncClient):
        """Test handling concurrent requests"""
        import time
        
        print("\n" + "="*60)
        print("⚡ Testing Concurrent Request Handling")
        print("="*60)
        
        # Create 10 concurrent prediction requests
        tasks = []
        for i in range(10):
            task = client.post(
                "/api/v1/predict-timeline",
                json={"project_id": f"proj_{i}"}
            )
            tasks.append(task)
        
        start_time = time.time()
        responses = await asyncio.gather(*tasks)
        end_time = time.time()
        
        # Verify all succeeded
        success_count = sum(1 for r in responses if r.status_code == 200)
        
        elapsed = (end_time - start_time) * 1000
        print(f"\n✅ {success_count}/10 requests succeeded in {elapsed:.0f}ms")
        print(f"   Average: {elapsed/10:.0f}ms per request")
        
        assert success_count >= 8, "Too many requests failed"


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
