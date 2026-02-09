"""
Test suite for API endpoints
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

from src.main import app

client = TestClient(app)


class TestPredictionEndpoints:
    """Test prediction API endpoints"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['status'] == 'healthy'
        assert 'service' in data
        assert 'models_loaded' in data
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['service'] == 'Intelligence Service'
        assert 'endpoints' in data
        assert 'docs' in data
    
    def test_predict_timeline(self):
        """Test timeline prediction endpoint"""
        request_data = {
            "project_id": "test_project_123",
            "target_date": (datetime.now() + timedelta(weeks=10)).isoformat()
        }
        
        response = client.post("/api/v1/predict-timeline", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['project_id'] == "test_project_123"
        assert 'predicted_completion_date' in data
        assert 'predicted_weeks_remaining' in data
        assert 'confidence_intervals' in data
        assert 'risk_factors' in data
        assert 'model_confidence' in data
        
        # Validate confidence intervals
        intervals = data['confidence_intervals']
        assert 'p10' in intervals
        assert 'p50' in intervals
        assert 'p90' in intervals
    
    def test_predict_timeline_without_target(self):
        """Test prediction without target date"""
        request_data = {
            "project_id": "test_project_456"
        }
        
        response = client.post("/api/v1/predict-timeline", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['project_id'] == "test_project_456"
        assert 'predicted_completion_date' in data
    
    def test_get_prediction_history(self):
        """Test prediction history endpoint"""
        response = client.get("/api/v1/prediction-history/test_project_123")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        if len(data) > 0:
            assert 'id' in data[0]
            assert 'project_id' in data[0]
            assert 'predicted_date' in data[0]
    
    def test_recalculate_timeline(self):
        """Test timeline recalculation endpoint"""
        response = client.post("/api/v1/recalculate-timeline/test_project_123")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['status'] == 'queued'
        assert data['project_id'] == 'test_project_123'


class TestSkillsEndpoints:
    """Test skills extraction endpoints"""
    
    def test_extract_skills(self):
        """Test skill extraction endpoint"""
        request_data = {
            "text": "Looking for a Python developer with FastAPI and Docker experience",
            "context": "job_description"
        }
        
        response = client.post("/api/v1/extract-skills", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'skills' in data
        assert 'confidence_scores' in data
        assert 'categories' in data
        assert isinstance(data['skills'], list)
    
    def test_skill_recommendations(self):
        """Test skill recommendations endpoint"""
        response = client.get("/api/v1/skill-recommendations/test_project_123")
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'project_id' in data
        assert 'missing_skills' in data
        assert 'skill_gaps' in data
        assert 'training_recommendations' in data


class TestSimulationEndpoints:
    """Test simulation endpoints"""
    
    def test_run_simulation(self):
        """Test simulation endpoint"""
        request_data = {
            "project_id": "test_project_123",
            "scenario": "add_team_member",
            "parameters": {
                "members_to_add": 2,
                "experience_level": "senior"
            }
        }
        
        response = client.post("/api/v1/run-simulation", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['scenario'] == 'add_team_member'
        assert 'original_completion' in data
        assert 'simulated_completion' in data
        assert 'impact_days' in data
        assert 'success_probability' in data
        assert 'recommendations' in data
    
    def test_simulation_history(self):
        """Test simulation history endpoint"""
        response = client.get("/api/v1/simulation-history/test_project_123")
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'project_id' in data
        assert 'simulations' in data


class TestSentimentEndpoints:
    """Test sentiment analysis endpoints"""
    
    def test_analyze_sentiment(self):
        """Test sentiment analysis endpoint"""
        request_data = {
            "text": "The team is doing great work and we're making excellent progress!",
            "context": "team_communication"
        }
        
        response = client.post("/api/v1/analyze-sentiment", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'sentiment' in data
        assert data['sentiment'] in ['positive', 'negative', 'neutral']
        assert 'score' in data
        assert 'confidence' in data
        assert 'emotions' in data
        
        # Validate score range
        assert -1 <= data['score'] <= 1
        assert 0 <= data['confidence'] <= 1
    
    def test_team_sentiment(self):
        """Test team sentiment endpoint"""
        response = client.get("/api/v1/team-sentiment/test_project_123?days=7")
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'project_id' in data
        assert 'overall_sentiment' in data
        assert 'morale_score' in data
        assert 'trend' in data
        assert 'daily_sentiment' in data
    
    def test_conversation_intelligence(self):
        """Test conversation intelligence endpoint"""
        response = client.post(
            "/api/v1/conversation-intelligence",
            params={"text": "We need to update the API docs and schedule a code review"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'action_items' in data
        assert 'decisions' in data
        assert 'blockers' in data
        assert 'questions' in data


class TestHealthEndpoints:
    """Test health monitoring endpoints"""
    
    def test_health_detailed(self):
        """Test detailed health endpoint"""
        response = client.get("/api/v1/health-detailed")
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'status' in data
        assert 'components' in data
        assert 'metrics' in data
        
        components = data['components']
        assert 'api' in components
        assert 'ml_models' in components
        assert 'database' in components
    
    def test_metrics(self):
        """Test metrics endpoint"""
        response = client.get("/api/v1/metrics")
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'predictions_total' in data
        assert 'predictions_success' in data
        assert 'avg_prediction_time_seconds' in data
    
    def test_model_performance(self):
        """Test model performance endpoint"""
        response = client.get("/api/v1/model-performance")
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'timeline_predictor' in data
        predictor_metrics = data['timeline_predictor']
        
        assert 'accuracy' in predictor_metrics
        assert 'predictions_count' in predictor_metrics
        assert 'status' in predictor_metrics


class TestInsightsEndpoints:
    """Test insights generation endpoints"""
    
    def test_project_insights(self):
        """Test project insights endpoint"""
        response = client.get("/api/v1/project-insights/test_project_123")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        if len(data) > 0:
            insight = data[0]
            assert 'type' in insight
            assert 'title' in insight
            assert 'description' in insight
            assert 'severity' in insight
            assert 'impact' in insight
            assert 'recommendations' in insight
    
    def test_team_insights(self):
        """Test team insights endpoint"""
        response = client.get("/api/v1/team-insights/test_team_123")
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'team_id' in data
        assert 'productivity_score' in data
        assert 'collaboration_health' in data
        assert 'workload_balance' in data
        assert 'skill_coverage' in data
    
    def test_risk_analysis(self):
        """Test risk analysis endpoint"""
        response = client.get("/api/v1/risk-analysis/test_project_123")
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'project_id' in data
        assert 'overall_risk_score' in data
        assert 'risk_level' in data
        assert 'risks' in data
        assert 'recommendations' in data
        
        # Validate risk score
        assert 0 <= data['overall_risk_score'] <= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
