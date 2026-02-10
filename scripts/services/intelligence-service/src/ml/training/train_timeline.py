"""
Timeline Model Training Script
Trains the RandomForest timeline predictor on historical project data
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from loguru import logger

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from src.ml.models.timeline_predictor import TimelinePredictor


def generate_synthetic_training_data(n_projects: int = 500) -> pd.DataFrame:
    """
    Generate synthetic historical project data for training
    
    Args:
        n_projects: Number of historical projects to generate
    
    Returns:
        DataFrame with project features and actual completion weeks
    """
    logger.info(f"🎲 Generating {n_projects} synthetic historical projects...")
    
    np.random.seed(42)
    data = []
    
    for i in range(n_projects):
        # Generate realistic project parameters
        team_size = np.random.randint(2, 15)
        total_tasks = np.random.randint(20, 300)
        completed_tasks = int(total_tasks * np.random.uniform(0.1, 0.9))
        remaining_tasks = total_tasks - completed_tasks
        
        # Velocity with realistic variation
        base_velocity = team_size * np.random.uniform(1.5, 3.0)
        avg_weekly_velocity = base_velocity * np.random.uniform(0.7, 1.3)
        velocity_std = avg_weekly_velocity * np.random.uniform(0.1, 0.3)
        
        # Story points
        remaining_story_points = remaining_tasks * np.random.uniform(3, 8)
        
        # Complexity factors
        blocked_tasks = np.random.randint(0, max(1, remaining_tasks // 5))
        high_priority_tasks = np.random.randint(0, remaining_tasks // 2)
        
        # Calculate actual completion time (ground truth)
        # Base time + complexity factors + randomness
        base_weeks = remaining_story_points / max(avg_weekly_velocity, 0.1)
        blocker_delay = blocked_tasks * np.random.uniform(0.5, 2.0)
        complexity_factor = np.random.uniform(0.8, 1.4)  # Project-specific factors
        
        actual_weeks = max(1, base_weeks * complexity_factor + blocker_delay + np.random.normal(0, 2))
        
        data.append({
            'team_size': team_size,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'remaining_tasks': remaining_tasks,
            'remaining_story_points': remaining_story_points,
            'avg_weekly_velocity': avg_weekly_velocity,
            'velocity_std': velocity_std,
            'blocked_tasks': blocked_tasks,
            'high_priority_tasks': high_priority_tasks,
            'active_sprints': np.random.uniform(0.5, 3.0),
            'actual_completion_weeks': actual_weeks  # Target variable
        })
    
    df = pd.DataFrame(data)
    logger.success(f"✅ Generated {len(df)} training examples")
    logger.info(f"   Average completion time: {df['actual_completion_weeks'].mean():.1f} weeks")
    logger.info(f"   Range: {df['actual_completion_weeks'].min():.1f} - {df['actual_completion_weeks'].max():.1f} weeks")
    
    return df


def train_timeline_model(save_path: str = None):
    """
    Train the timeline prediction model on synthetic data
    
    Args:
        save_path: Path to save the trained model (default: src/data/models)
    """
    logger.info("=" * 60)
    logger.info("🚀 Training Timeline Prediction Model")
    logger.info("=" * 60)
    
    # Generate training data
    training_data = generate_synthetic_training_data(n_projects=500)
    
    # Initialize model
    logger.info("\n📦 Initializing TimelinePredictor...")
    predictor = TimelinePredictor()
    
    # Train the model
    logger.info("\n🎓 Training model...")
    predictor.train(training_data)
    
    # Test predictions on a few examples
    logger.info("\n🧪 Testing model on sample data...")
    test_samples = training_data.sample(5)
    
    for idx, row in test_samples.iterrows():
        project_data = row.to_dict()
        actual = project_data.pop('actual_completion_weeks')
        
        prediction = predictor.predict_completion_date(project_data, run_monte_carlo=False)
        predicted_weeks = prediction['predicted_weeks_remaining']
        
        error = abs(predicted_weeks - actual)
        logger.info(f"   Project {idx}: Predicted={predicted_weeks:.1f} weeks, Actual={actual:.1f} weeks, Error={error:.1f} weeks")
    
    # Save the model
    if save_path is None:
        save_path = os.path.join(
            os.path.dirname(__file__),
            "../../../src/data/models"
        )
    
    os.makedirs(save_path, exist_ok=True)
    model_file = os.path.join(save_path, "timeline_model.pkl")
    
    logger.info(f"\n💾 Saving trained model to: {model_file}")
    predictor.save(model_file)
    
    logger.success("\n✅ Training complete!")
    logger.info(f"   Model saved to: {model_file}")
    logger.info(f"   Feature names: {predictor.feature_names}")
    logger.info(f"   Model trained: {predictor.is_trained}")
    
    return predictor


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    
    trained_model = train_timeline_model()
    
    print("\n" + "=" * 60)
    print("✅ Timeline Model Training Complete!")
    print("=" * 60)
    print("\nTo use the trained model:")
    print("1. Restart the Intelligence Service")
    print("2. The model will automatically load from src/data/models/timeline_model.pkl")
    print("3. Predictions will now use the trained ML model instead of heuristics")
    print("=" * 60)
