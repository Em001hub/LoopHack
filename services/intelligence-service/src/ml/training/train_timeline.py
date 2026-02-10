"""
Timeline Prediction Model Training Script
Trains Random Forest model on historical project data
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from loguru import logger
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.ml.models.timeline_predictor import TimelinePredictor
from src.ml.utils.feature_engineering import FeatureEngineer


class TimelineModelTrainer:
    """
    Train and evaluate timeline prediction model
    """
    
    def __init__(self, model_save_path: str = "./src/data/models"):
        self.model_save_path = Path(model_save_path)
        self.model_save_path.mkdir(parents=True, exist_ok=True)
        
        self.model = None
        self.scaler = StandardScaler()
        self.feature_engineer = FeatureEngineer()
        
        logger.info("🎓 Timeline Model Trainer initialized")
    
    def load_training_data(self, data_path: str = "./src/data/datasets/historical_projects.csv") -> pd.DataFrame:
        """
        Load prepared training data
        
        **Expected columns:**
        - remaining_story_points
        - avg_weekly_velocity
        - velocity_std
        - team_size
        - blocked_tasks_count
        - high_complexity_count
        - avg_task_age_days
        - team_experience_score
        - actual_weeks_taken (TARGET)
        """
        logger.info(f"📂 Loading training data from {data_path}")
        
        try:
            df = pd.read_csv(data_path)
            logger.success(f"✅ Loaded {len(df)} training samples")
            return df
        except FileNotFoundError:
            logger.error(f"❌ Training data not found at {data_path}")
            logger.info("💡 Run data_preparation.py first to generate training data")
            raise
    
    def prepare_features_and_target(self, df: pd.DataFrame):
        """
        Separate features (X) and target (y)
        """
        logger.info("🔧 Preparing features and target")
        
        # Feature columns
        feature_columns = [
            'remaining_story_points',
            'avg_weekly_velocity',
            'velocity_std',
            'team_size',
            'blocked_tasks_count',
            'high_complexity_count',
            'avg_task_age_days',
            'team_experience_score'
        ]
        
        # Ensure all columns exist
        missing_cols = [col for col in feature_columns if col not in df.columns]
        if missing_cols:
            logger.error(f"❌ Missing columns: {missing_cols}")
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        X = df[feature_columns].values
        y = df['actual_weeks_taken'].values
        
        logger.info(f"✅ Features shape: {X.shape}, Target shape: {y.shape}")
        
        return X, y, feature_columns
    
    def train_model(self, X_train, y_train, X_val, y_val):
        """
        Train Random Forest model
        """
        logger.info("🚀 Training Random Forest model...")
        
        # Create model
        self.model = RandomForestRegressor(
            n_estimators=200,        # Number of trees
            max_depth=15,            # Maximum tree depth
            min_samples_split=5,     # Minimum samples to split
            min_samples_leaf=2,      # Minimum samples in leaf
            max_features='sqrt',     # Features to consider for split
            random_state=42,
            n_jobs=-1,               # Use all CPU cores
            verbose=1
        )
        
        # Train
        self.model.fit(X_train, y_train)
        
        logger.success("✅ Model training complete")
        
        # Evaluate on training set
        train_score = self.model.score(X_train, y_train)
        logger.info(f"📊 Training R² Score: {train_score:.4f}")
        
        # Evaluate on validation set
        val_score = self.model.score(X_val, y_val)
        logger.info(f"📊 Validation R² Score: {val_score:.4f}")
        
        return self.model
    
    def evaluate_model(self, X_test, y_test):
        """
        Comprehensive model evaluation
        """
        logger.info("📊 Evaluating model performance...")
        
        # Make predictions
        y_pred = self.model.predict(X_test)
        
        # Calculate metrics
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        # Mean Absolute Percentage Error
        mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
        
        # Accuracy within X weeks
        within_1_week = np.mean(np.abs(y_test - y_pred) <= 1) * 100
        within_2_weeks = np.mean(np.abs(y_test - y_pred) <= 2) * 100
        within_3_weeks = np.mean(np.abs(y_test - y_pred) <= 3) * 100
        
        # Print results
        logger.info("\n" + "="*60)
        logger.info("📊 MODEL EVALUATION RESULTS")
        logger.info("="*60)
        logger.info(f"R² Score:              {r2:.4f}")
        logger.info(f"Mean Absolute Error:   {mae:.2f} weeks")
        logger.info(f"Root Mean Squared Error: {rmse:.2f} weeks")
        logger.info(f"Mean Absolute % Error: {mape:.2f}%")
        logger.info("\n📈 PREDICTION ACCURACY:")
        logger.info(f"Within ±1 week:        {within_1_week:.1f}%")
        logger.info(f"Within ±2 weeks:       {within_2_weeks:.1f}%")
        logger.info(f"Within ±3 weeks:       {within_3_weeks:.1f}%")
        logger.info("="*60 + "\n")
        
        metrics = {
            'r2_score': r2,
            'mae': mae,
            'rmse': rmse,
            'mape': mape,
            'within_1_week': within_1_week,
            'within_2_weeks': within_2_weeks,
            'within_3_weeks': within_3_weeks
        }
        
        return metrics, y_pred
    
    def plot_results(self, y_test, y_pred, feature_names):
        """
        Create visualization plots
        """
        logger.info("📈 Creating visualization plots...")
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Actual vs Predicted
        axes[0, 0].scatter(y_test, y_pred, alpha=0.6)
        axes[0, 0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
        axes[0, 0].set_xlabel('Actual Weeks', fontsize=12)
        axes[0, 0].set_ylabel('Predicted Weeks', fontsize=12)
        axes[0, 0].set_title('Actual vs Predicted Timeline', fontsize=14, fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Residuals
        residuals = y_test - y_pred
        axes[0, 1].scatter(y_pred, residuals, alpha=0.6)
        axes[0, 1].axhline(y=0, color='r', linestyle='--', lw=2)
        axes[0, 1].set_xlabel('Predicted Weeks', fontsize=12)
        axes[0, 1].set_ylabel('Residuals', fontsize=12)
        axes[0, 1].set_title('Residual Plot', fontsize=14, fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Feature Importance
        feature_importance = self.model.feature_importances_
        sorted_idx = np.argsort(feature_importance)
        pos = np.arange(sorted_idx.shape[0]) + 0.5
        
        axes[1, 0].barh(pos, feature_importance[sorted_idx], align='center')
        axes[1, 0].set_yticks(pos)
        axes[1, 0].set_yticklabels(np.array(feature_names)[sorted_idx])
        axes[1, 0].set_xlabel('Importance', fontsize=12)
        axes[1, 0].set_title('Feature Importance', fontsize=14, fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3, axis='x')
        
        # 4. Error Distribution
        axes[1, 1].hist(residuals, bins=30, edgecolor='black', alpha=0.7)
        axes[1, 1].axvline(x=0, color='r', linestyle='--', lw=2)
        axes[1, 1].set_xlabel('Prediction Error (weeks)', fontsize=12)
        axes[1, 1].set_ylabel('Frequency', fontsize=12)
        axes[1, 1].set_title('Error Distribution', fontsize=14, fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        # Save plot
        plot_path = self.model_save_path / "training_results.png"
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        logger.success(f"✅ Plots saved to {plot_path}")
        
        plt.close()
    
    def save_model(self):
        """
        Save trained model and scaler
        """
        logger.info("💾 Saving trained model...")
        
        # Save to TimelinePredictor format
        predictor = TimelinePredictor()
        predictor.model = self.model
        predictor.scaler = self.scaler
        predictor.is_trained = True
        
        model_path = self.model_save_path / "timeline_model.pkl"
        predictor.save(str(model_path))
        
        logger.success(f"✅ Model saved to {model_path}")
    
    def run_full_training(self, data_path: str = "./src/data/datasets/historical_projects.csv"):
        """
        Complete training pipeline
        """
        logger.info("\n" + "="*60)
        logger.info("🎓 STARTING TIMELINE MODEL TRAINING")
        logger.info("="*60 + "\n")
        
        # 1. Load data
        df = self.load_training_data(data_path)
        
        # 2. Prepare features
        X, y, feature_names = self.prepare_features_and_target(df)
        
        # 3. Split data (70% train, 15% val, 15% test)
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y, test_size=0.15, random_state=42
        )
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=0.176, random_state=42  # 0.176 * 0.85 ≈ 0.15
        )
        
        logger.info(f"📊 Data split:")
        logger.info(f"   Training:   {len(X_train)} samples ({len(X_train)/len(X)*100:.1f}%)")
        logger.info(f"   Validation: {len(X_val)} samples ({len(X_val)/len(X)*100:.1f}%)")
        logger.info(f"   Test:       {len(X_test)} samples ({len(X_test)/len(X)*100:.1f}%)\n")
        
        # 4. Scale features
        logger.info("🔧 Scaling features...")
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        X_test_scaled = self.scaler.transform(X_test)
        logger.success("✅ Features scaled\n")
        
        # 5. Train model
        self.train_model(X_train_scaled, y_train, X_val_scaled, y_val)
        
        # 6. Evaluate on test set
        metrics, y_pred = self.evaluate_model(X_test_scaled, y_test)
        
        # 7. Create visualizations
        self.plot_results(y_test, y_pred, feature_names)
        
        # 8. Save model
        self.save_model()
        
        logger.info("\n" + "="*60)
        logger.info("🎉 TRAINING COMPLETE!")
        logger.info("="*60)
        logger.info(f"✅ Model saved and ready for deployment")
        logger.info(f"✅ Prediction accuracy: {metrics['within_2_weeks']:.1f}% within ±2 weeks")
        logger.info(f"✅ R² Score: {metrics['r2_score']:.4f}")
        logger.info("="*60 + "\n")
        
        return metrics


def main():
    """Main training function"""
    
    # Create trainer
    trainer = TimelineModelTrainer()
    
    # Run training
    metrics = trainer.run_full_training()
    
    return metrics


if __name__ == "__main__":
    main()
