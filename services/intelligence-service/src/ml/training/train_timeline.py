"""
Timeline Predictor Training Script
Trains the Random Forest model on historical project data
"""
import pandas as pd
import numpy as np
import pickle
import argparse
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from loguru import logger
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

try:
    from ml.utils.feature_engineering import FeatureEngineer
    from ml.training.model_evaluation import ModelEvaluator
    from ml.utils.data_transformers import LogTransformer
except:
    logger.warning("Could not import from ml package, using fallback")


def load_training_data(path: str) -> pd.DataFrame:
    """Load and validate training data CSV"""
    logger.info(f"📂 Loading data from {path}")
    try:
        df = pd.read_csv(path)
        required_cols = [
            'remaining_story_points', 'avg_weekly_velocity', 'team_size',
            'actual_weeks_taken'  # Target
        ]
        
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
            
        return df
    except Exception as e:
        logger.error(f"Failed to load data: {e}")
        sys.exit(1)


def train_model(data_path: str, output_path: str):
    """Main training pipeline"""
    logger.info("🚀 Starting Timeline Predictor training...")
    
    # 1. Load Data
    df = load_training_data(data_path)
    
    # 2. Feature Engineering
    features = [
        'remaining_story_points', 'avg_weekly_velocity', 'velocity_std',
        'team_size', 'blocked_tasks_count', 'high_complexity_count',
        'avg_task_age_days', 'team_experience_score'
    ]
    target = 'actual_weeks_taken'
    
    # Fill missing columns with defaults
    for col in features:
        if col not in df.columns:
            df[col] = 0
    
    X = df[features]
    y = df[target]
    
    # 3. Split Data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # 4. Build Pipeline
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', RandomForestRegressor(random_state=42))
    ])
    
    # 5. Hyperparameter Tuning
    param_grid = {
        'regressor__n_estimators': [100, 200],
        'regressor__max_depth': [None, 10, 20],
        'regressor__min_samples_split': [2, 5]
    }
    
    logger.info("⚙️ Tuning hyperparameters...")
    grid_search = GridSearchCV(pipeline, param_grid, cv=3, scoring='neg_mean_squared_error', n_jobs=-1)
    grid_search.fit(X_train, y_train)
    
    best_model = grid_search.best_estimator_
    logger.success(f"✅ Best params: {grid_search.best_params_}")
    
    # 6. Evaluate
    y_pred = best_model.predict(X_test)
    
    # Calculate metrics manually
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    metrics = {
        'mse': float(mse),
        'rmse': float(rmse),
        'mae': float(mae),
        'r2': float(r2),
        'mape': 0.0
    }
    
    logger.info(f"📊 Metrics: RMSE={rmse:.2f}, MAE={mae:.2f}, R2={r2:.2f}")
    
    if metrics['r2'] < 0.5:
        logger.warning("⚠️  Model performance is low (R2 < 0.5)")
    
    # 7. Save Model
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as f:
        pickle.dump({
            'model': best_model,
            'features': features,
            'metrics': metrics,
            'trained_at': pd.Timestamp.now().isoformat()
        }, f)
        
    logger.success(f"💾 Model saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Timeline Predictor")
    parser.add_argument("--data", type=str, required=True, help="Path to training CSV")
    parser.add_argument("--output", type=str, default="src/data/models/timeline_model.pkl")
    
    args = parser.parse_args()
    train_model(args.data, args.output)
