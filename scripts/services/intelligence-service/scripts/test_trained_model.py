"""
Test the trained Timeline Prediction model
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.ml.models.timeline_predictor import TimelinePredictor

def test_trained_model():
    """Test the trained model with sample project data"""
    
    print("\n" + "=" * 60)
    print("🧪 Testing Trained Timeline Prediction Model")
    print("=" * 60)
    
    # Load the trained model
    print("\n📦 Loading trained model...")
    predictor = TimelinePredictor()
    
    model_path = "src/data/models/timeline_model.pkl"
    if os.path.exists(model_path):
        predictor.load(model_path)
        print(f"✅ Model loaded from: {model_path}")
        print(f"   Model is trained: {predictor.is_trained}")
    else:
        print(f"⚠️  No trained model found at {model_path}")
        print("   Using heuristic predictions instead")
    
    # Test with sample projects
    test_projects = [
        {
            "name": "Small Agile Project",
            "team_size": 5,
            "total_tasks": 50,
            "completed_tasks": 30,
            "remaining_tasks": 20,
            "remaining_story_points": 40,
            "avg_weekly_velocity": 8.5,
            "velocity_std": 1.2,
            "blocked_tasks": 2,
            "high_priority_tasks": 8,
            "active_sprints": 2.0
        },
        {
            "name": "Large Enterprise Project",
            "team_size": 12,
            "total_tasks": 250,
            "completed_tasks": 100,
            "remaining_tasks": 150,
            "remaining_story_points": 600,
            "avg_weekly_velocity": 25.0,
            "velocity_std": 5.0,
            "blocked_tasks": 15,
            "high_priority_tasks": 50,
            "active_sprints": 1.5
        },
        {
            "name": "Startup MVP",
            "team_size": 3,
            "total_tasks": 80,
            "completed_tasks": 60,
            "remaining_tasks": 20,
            "remaining_story_points": 50,
            "avg_weekly_velocity": 6.0,
            "velocity_std": 2.0,
            "blocked_tasks": 3,
            "high_priority_tasks": 15,
            "active_sprints": 3.0
        }
    ]
    
    print("\n📊 Predictions:\n")
    for project in test_projects:
        name = project.pop("name")
        prediction = predictor.predict_completion_date(project, run_monte_carlo=True)
        
        print(f"  🎯 {name}")
        print(f"     Predicted completion: {prediction['predicted_completion_date']}")
        print(f"     Weeks remaining: {prediction['predicted_weeks_remaining']:.1f}")
        print(f"     Confidence: {prediction['model_confidence']:.0%}")
        print(f"     P10-P90 range: {prediction['confidence_intervals']['p10']} to {prediction['confidence_intervals']['p90']}")
        if prediction['probability_on_time'] is not None:
            print(f"     On-time probability: {prediction['probability_on_time']:.0%}")
        print()
    
    print("=" * 60)
    print("✅ Model testing complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_trained_model()
