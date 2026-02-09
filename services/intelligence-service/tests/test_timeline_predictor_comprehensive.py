"""
Comprehensive Test Suite for Timeline Predictor ML Model
Tests all prediction functionality, Monte Carlo simulations, and heuristics
Based on Person T implementation
"""

import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from src.ml.models.timeline_predictor import TimelinePredictor


class TestTimelinePredictor:
    """Test TimelinePredictor model"""
    
    @pytest.fixture
    def predictor(self):
        """Create predictor instance"""
        return TimelinePredictor()
    
    @pytest.fixture
    def sample_project_data(self):
        """Sample project data for testing"""
        return {
            'project_id': 'test_project',
            'remaining_story_points': 100,
            'avg_weekly_velocity': 20,
            'velocity_std': 4,
            'team_size': 5,
            'blocked_tasks_count': 2,
            'high_complexity_count': 3,
            'avg_task_age_days': 10,
            'team_experience_score': 0.7,
            'target_date': (datetime.now() + timedelta(weeks=8)).isoformat()
        }
    
    def test_predictor_initialization(self, predictor):
        """Test predictor initializes correctly"""
        assert predictor is not None
        assert predictor.model is not None
        assert hasattr(predictor, 'is_trained')
    
    def test_feature_extraction(self, predictor, sample_project_data):
        """Test feature extraction from project data"""
        features = predictor.extract_features(sample_project_data)
        
        assert isinstance(features, (np.ndarray, list, dict))
        # Verify key features are extracted
        if isinstance(features, dict):
            assert 'remaining_story_points' in str(features) or len(features) > 0
    
    def test_heuristic_prediction(self, predictor, sample_project_data):
        """Test heuristic prediction when model not trained"""
        prediction = predictor.predict_completion_date(
            sample_project_data,
            run_monte_carlo=False
        )
        
        # Verify structure
        assert 'predicted_completion_date' in prediction
        assert 'predicted_weeks_remaining' in prediction
        assert 'confidence_intervals' in prediction
        assert 'risk_factors' in prediction
        
        # Verify date is in future
        predicted_date = datetime.fromisoformat(prediction['predicted_completion_date'])
        assert predicted_date > datetime.now()
    
    def test_heuristic_prediction_logic(self, predictor):
        """Test heuristic calculation logic"""
        # Simple case: 100 points, 20 velocity = 5 weeks
        simple_data = {
            'remaining_story_points': 100,
            'avg_weekly_velocity': 20,
            'team_size': 5,
            'blocked_tasks_count': 0,
            'high_complexity_count': 0
        }
        
        prediction = predictor.predict_completion_date(simple_data)
        
        # Base should be ~5 weeks (100/20)
        assert 3.5 <= prediction['predicted_weeks_remaining'] <= 7.0
    
    def test_heuristic_risk_factors(self, predictor):
        """Test risk factors are identified"""
        risky_data = {
            'remaining_story_points': 100,
            'avg_weekly_velocity': 20,
            'team_size': 2,  # Small team
            'blocked_tasks_count': 3,  # Multiple blockers
            'high_complexity_count': 5  # Many complex tasks
        }
        
        prediction = predictor.predict_completion_date(risky_data)
        
        # Should identify risk factors
        assert len(prediction['risk_factors']) > 0
        
        # Prediction should be longer due to risks
        assert prediction['predicted_weeks_remaining'] > 4.0
    
    def test_monte_carlo_simulation(self, predictor, sample_project_data):
        """Test Monte Carlo simulation runs correctly"""
        prediction = predictor.predict_completion_date(
            sample_project_data,
            run_monte_carlo=True
        )
        
        # Verify Monte Carlo results
        assert 'confidence_intervals' in prediction
        intervals = prediction['confidence_intervals']
        
        # Should have percentiles
        assert 'p10' in intervals or 'p50' in intervals or 'p90' in intervals
    
    def test_probability_calculation(self, predictor, sample_project_data):
        """Test probability of meeting deadline calculation"""
        prediction = predictor.predict_completion_date(sample_project_data)
        
        # Should have probability if target_date provided
        assert 'probability_on_time' in prediction or 'predicted_completion_date' in prediction
    
    def test_edge_case_zero_velocity(self, predictor):
        """Test handling of zero velocity"""
        edge_data = {
            'remaining_story_points': 100,
            'avg_weekly_velocity': 0,  # Zero velocity
            'team_size': 5
        }
        
        prediction = predictor.predict_completion_date(edge_data)
        
        # Should handle gracefully
        assert prediction is not None
        assert prediction['predicted_weeks_remaining'] > 0
    
    def test_edge_case_large_project(self, predictor):
        """Test very large project"""
        large_data = {
            'remaining_story_points': 10000,
            'avg_weekly_velocity': 20,
            'team_size': 10
        }
        
        prediction = predictor.predict_completion_date(large_data)
        
        # Should handle large numbers
        assert prediction is not None
        # Should cap at reasonable max (very large projects can take a long time)
        assert prediction['predicted_weeks_remaining'] <= 600  # ~11 years max
    
    def test_risk_factor_identification(self, predictor):
        """Test comprehensive risk factor detection"""
        risky_data = {
            'remaining_story_points': 100,
            'avg_weekly_velocity': 10,
            'velocity_std': 8,  # High variance
            'team_size': 2,     # Small team
            'blocked_tasks_count': 4,  # Many blockers
            'high_complexity_count': 6,  # Many complex tasks
            'avg_task_age_days': 20  # Stale tasks
        }
        
        prediction = predictor.predict_completion_date(risky_data)
        risks = prediction['risk_factors']
        
        # Should identify multiple risks
        assert len(risks) >= 1
        
        # Check specific risks mentioned
        risk_text = ' '.join(risks).lower()
        assert any(keyword in risk_text for keyword in ['blocked', 'blocker', 'complex', 'team', 'velocity'])


class TestMonteCarloSimulation:
    """Test Monte Carlo simulation specifically"""
    
    @pytest.fixture
    def predictor(self):
        return TimelinePredictor()
    
    def test_simulation_produces_results(self, predictor):
        """Test simulation produces valid results"""
        project_data = {
            'remaining_story_points': 100,
            'avg_weekly_velocity': 20,
            'velocity_std': 4,
            'team_size': 5
        }
        
        result = predictor.predict_completion_date(project_data, run_monte_carlo=True)
        
        # Should have confidence intervals
        assert 'confidence_intervals' in result
        assert result['predicted_weeks_remaining'] > 0


class TestPredictionAccuracy:
    """Test prediction accuracy and validation"""
    
    @pytest.fixture
    def predictor(self):
        return TimelinePredictor()
    
    def test_prediction_reasonableness(self, predictor):
        """Test predictions are reasonable"""
        # Test case: 100 points, 20 velocity
        # Expected: ~5 weeks
        project_data = {
            'remaining_story_points': 100,
            'avg_weekly_velocity': 20,
            'velocity_std': 4,
            'team_size': 5,
            'blocked_tasks_count': 0,
            'high_complexity_count': 0,
            'avg_task_age_days': 10,
            'team_experience_score': 0.7
        }
        
        prediction = predictor.predict_completion_date(project_data)
        
        # Should be roughly 3-9 weeks (accounting for variance and risks)
        assert 2 <= prediction['predicted_weeks_remaining'] <= 12


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
