"""
Test suite for Timeline Predictor ML model
"""

import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from src.ml.models.timeline_predictor import TimelinePredictor


class TestTimelinePredictor:
    """Test cases for TimelinePredictor"""
    
    @pytest.fixture
    def predictor(self):
        """Create a fresh predictor instance for each test"""
        return TimelinePredictor()
    
    @pytest.fixture
    def sample_project_data(self):
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
    
    def test_predictor_initialization(self, predictor):
        """Test that predictor initializes correctly"""
        assert predictor is not None
        assert predictor.is_trained == False
        assert len(predictor.feature_names) == 8
        assert predictor.model is not None
        assert predictor.scaler is not None
    
    def test_feature_extraction(self, predictor, sample_project_data):
        """Test feature extraction from project data"""
        features = predictor.extract_features(sample_project_data)
        
        assert features.shape == (1, 8)
        assert features[0, 0] == 100  # remaining_story_points
        assert features[0, 1] == 20   # avg_weekly_velocity
        assert features[0, 3] == 5    # team_size
    
    def test_feature_extraction_with_missing_data(self, predictor):
        """Test feature extraction handles missing data gracefully"""
        incomplete_data = {
            'remaining_story_points': 50,
            'avg_weekly_velocity': 10
        }
        
        features = predictor.extract_features(incomplete_data)
        
        assert features.shape == (1, 8)
        assert features[0, 0] == 50
        assert features[0, 1] == 10
        # Missing values should default to 0 or defaults
        assert features[0, 3] == 1  # team_size defaults to 1
    
    def test_heuristic_prediction(self, predictor, sample_project_data):
        """Test heuristic prediction (when model not trained)"""
        result = predictor.predict_completion_date(sample_project_data)
        
        assert 'predicted_completion_date' in result
        assert 'predicted_weeks_remaining' in result
        assert 'confidence_intervals' in result
        assert 'risk_factors' in result
        assert 'model_confidence' in result
        
        # Should use heuristic since not trained
        assert result['model_confidence'] == 0.60
        assert result.get('note') == 'Heuristic prediction (model not trained)'
    
    def test_heuristic_calculation(self, predictor):
        """Test heuristic calculation logic"""
        simple_data = {
            'remaining_story_points': 100,
            'avg_weekly_velocity': 20,
            'velocity_std': 0,
            'team_size': 5,
            'blocked_tasks_count': 0,
            'high_complexity_count': 0,
            'avg_task_age_days': 0,
            'team_experience_score': 0.5
        }
        
        result = predictor.predict_completion_date(simple_data)
        
        # Base: 100 / 20 = 5 weeks
        # No risk multipliers, so should be ~5 weeks
        assert 4 <= result['predicted_weeks_remaining'] <= 6
    
    def test_risk_factor_identification(self, predictor, sample_project_data):
        """Test risk factor identification"""
        result = predictor.predict_completion_date(sample_project_data)
        
        risk_factors = result['risk_factors']
        
        # Should identify blocked tasks
        assert any('blocked' in risk.lower() for risk in risk_factors)
        
        # Should identify high complexity
        assert any('complexity' in risk.lower() for risk in risk_factors)
    
    def test_monte_carlo_simulation(self, predictor, sample_project_data):
        """Test Monte Carlo simulation"""
        result = predictor.predict_completion_date(
            sample_project_data,
            run_monte_carlo=True
        )
        
        intervals = result['confidence_intervals']
        
        # Check that all percentiles exist
        assert 'p10' in intervals
        assert 'p50' in intervals
        assert 'p90' in intervals
        
        # P10 should be before P50, P50 before P90
        p10 = datetime.fromisoformat(intervals['p10'])
        p50 = datetime.fromisoformat(intervals['p50'])
        p90 = datetime.fromisoformat(intervals['p90'])
        
        assert p10 <= p50 <= p90
    
    def test_probability_calculation(self, predictor, sample_project_data):
        """Test probability of meeting target date"""
        target_date = datetime.now() + timedelta(weeks=10)
        sample_project_data['target_date'] = target_date
        
        result = predictor.predict_completion_date(sample_project_data)
        
        # Should have probability
        assert 'probability_on_time' in result
        
        # Probability should be between 0 and 1 (or None)
        prob = result['probability_on_time']
        if prob is not None:
            assert 0 <= prob <= 1
    
    def test_model_training(self, predictor):
        """Test model training with synthetic data"""
        # Create synthetic training data
        np.random.seed(42)
        n_samples = 100
        
        training_data = pd.DataFrame({
            'remaining_story_points': np.random.randint(50, 200, n_samples),
            'avg_weekly_velocity': np.random.randint(10, 30, n_samples),
            'velocity_std': np.random.randint(1, 5, n_samples),
            'team_size': np.random.randint(3, 10, n_samples),
            'blocked_tasks_count': np.random.randint(0, 5, n_samples),
            'high_complexity_count': np.random.randint(0, 10, n_samples),
            'avg_task_age_days': np.random.randint(0, 20, n_samples),
            'team_experience_score': np.random.uniform(0.3, 1.0, n_samples),
            'actual_weeks_taken': np.random.randint(5, 15, n_samples)
        })
        
        result = predictor.train(training_data)
        
        assert result['status'] == 'success'
        assert result['samples'] == n_samples
        assert predictor.is_trained == True
        assert 'r2_score' in result
    
    def test_model_save_load(self, predictor, tmp_path):
        """Test model save and load functionality"""
        # Train model first
        np.random.seed(42)
        training_data = pd.DataFrame({
            'remaining_story_points': np.random.randint(50, 200, 50),
            'avg_weekly_velocity': np.random.randint(10, 30, 50),
            'velocity_std': np.random.randint(1, 5, 50),
            'team_size': np.random.randint(3, 10, 50),
            'blocked_tasks_count': np.random.randint(0, 5, 50),
            'high_complexity_count': np.random.randint(0, 10, 50),
            'avg_task_age_days': np.random.randint(0, 20, 50),
            'team_experience_score': np.random.uniform(0.3, 1.0, 50),
            'actual_weeks_taken': np.random.randint(5, 15, 50)
        })
        
        predictor.train(training_data)
        
        # Save model
        model_path = tmp_path / "test_model.pkl"
        predictor.save(str(model_path))
        
        assert model_path.exists()
        
        # Load model in new instance
        new_predictor = TimelinePredictor()
        assert new_predictor.is_trained == False
        
        new_predictor.load(str(model_path))
        assert new_predictor.is_trained == True
    
    def test_edge_case_zero_velocity(self, predictor):
        """Test handling of edge case: zero velocity"""
        edge_data = {
            'remaining_story_points': 100,
            'avg_weekly_velocity': 0,  # Edge case
            'velocity_std': 0,
            'team_size': 1,
            'blocked_tasks_count': 0,
            'high_complexity_count': 0,
            'avg_task_age_days': 0,
            'team_experience_score': 0.5
        }
        
        # Should not crash, should handle gracefully
        result = predictor.predict_completion_date(edge_data)
        
        assert result is not None
        assert 'predicted_weeks_remaining' in result
    
    def test_edge_case_negative_values(self, predictor):
        """Test handling of negative values (invalid input)"""
        invalid_data = {
            'remaining_story_points': -50,  # Invalid
            'avg_weekly_velocity': 10,
            'velocity_std': 0,
            'team_size': 5,
            'blocked_tasks_count': 0,
            'high_complexity_count': 0,
            'avg_task_age_days': 0,
            'team_experience_score': 0.5
        }
        
        # Should still produce a result (model is robust)
        result = predictor.predict_completion_date(invalid_data)
        assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
