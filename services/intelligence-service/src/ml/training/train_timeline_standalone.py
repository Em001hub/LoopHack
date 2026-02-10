"""
Standalone Timeline Model Training Script (No Database Required)
Trains Random Forest model on prepared CSV data
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from pathlib import Path

print("🎓 Starting Timeline Model Training (Standalone Mode)")
print("=" * 60)

# Paths
data_path = Path("./src/data/datasets/historical_projects.csv")
model_save_path = Path("./src/data/models")
model_save_path.mkdir(parents=True, exist_ok=True)

def load_training_data():
    """Load prepared training data"""
    print(f"📂 Loading training data from {data_path}")
    
    if not data_path.exists():
        print(f"❌ Training data not found at {data_path}")
        print("💡 Run data_preparation_standalone.py first!")
        raise FileNotFoundError(f"Training data not found: {data_path}")
    
    df = pd.read_csv(data_path)
    print(f"✅ Loaded {len(df)} training samples")
    return df

def prepare_features_and_target(df):
    """Separate features (X) and target (y)"""
    print("🔧 Preparing features and target")
    
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
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    X = df[feature_columns].values
    y = df['actual_weeks_taken'].values
    
    print(f"✅ Features shape: {X.shape}, Target shape: {y.shape}")
    
    return X, y, feature_columns

def train_model(X_train, y_train, X_val, y_val):
    """Train Random Forest model"""
    print("🚀 Training Random Forest model...")
    
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        max_features='sqrt',
        random_state=42,
        n_jobs=-1,
        verbose=0
    )
    
    model.fit(X_train, y_train)
    
    print("✅ Model training complete")
    
    # Evaluate on training set
    train_score = model.score(X_train, y_train)
    print(f"📊 Training R² Score: {train_score:.4f}")
    
    # Evaluate on validation set
    val_score = model.score(X_val, y_val)
    print(f"📊 Validation R² Score: {val_score:.4f}")
    
    return model

def evaluate_model(model, X_test, y_test):
    """Comprehensive model evaluation"""
    print("📊 Evaluating model performance...")
    
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    mape = np.mean(np.abs((y_test - y_pred) / np.maximum(y_test, 1e-10))) * 100
    
    # Accuracy within X weeks
    within_1_week = np.mean(np.abs(y_test - y_pred) <= 1) * 100
    within_2_weeks = np.mean(np.abs(y_test - y_pred) <= 2) * 100
    within_3_weeks = np.mean(np.abs(y_test - y_pred) <= 3) * 100
    
    # Print results
    print("\n" + "=" * 60)
    print("📊 MODEL EVALUATION RESULTS")
    print("=" * 60)
    print(f"R² Score:              {r2:.4f}")
    print(f"Mean Absolute Error:   {mae:.2f} weeks")
    print(f"Root Mean Squared Error: {rmse:.2f} weeks")
    print(f"Mean Absolute % Error: {mape:.2f}%")
    print("\n📈 PREDICTION ACCURACY:")
    print(f"Within ±1 week:        {within_1_week:.1f}%")
    print(f"Within ±2 weeks:       {within_2_weeks:.1f}%")
    print(f"Within ±3 weeks:       {within_3_weeks:.1f}%")
    print("=" * 60)
    
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

def plot_results(y_test, y_pred, feature_names, feature_importance):
    """Create visualization plots"""
    print("📈 Creating visualization plots...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Actual vs Predicted
    axes[0, 0].scatter(y_test, y_pred, alpha=0.6, color='blue')
    axes[0, 0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    axes[0, 0].set_xlabel('Actual Weeks', fontsize=12)
    axes[0, 0].set_ylabel('Predicted Weeks', fontsize=12)
    axes[0, 0].set_title('Actual vs Predicted Timeline', fontsize=14, fontweight='bold')
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Residuals
    residuals = y_test - y_pred
    axes[0, 1].scatter(y_pred, residuals, alpha=0.6, color='green')
    axes[0, 1].axhline(y=0, color='r', linestyle='--', lw=2)
    axes[0, 1].set_xlabel('Predicted Weeks', fontsize=12)
    axes[0, 1].set_ylabel('Residuals', fontsize=12)
    axes[0, 1].set_title('Residual Plot', fontsize=14, fontweight='bold')
    axes[0, 1].grid(True, alpha=0.3)
    
    # 3. Feature Importance
    sorted_idx = np.argsort(feature_importance)
    pos = np.arange(sorted_idx.shape[0]) + 0.5
    
    axes[1, 0].barh(pos, feature_importance[sorted_idx], align='center', color='orange')
    axes[1, 0].set_yticks(pos)
    axes[1, 0].set_yticklabels(np.array(feature_names)[sorted_idx])
    axes[1, 0].set_xlabel('Importance', fontsize=12)
    axes[1, 0].set_title('Feature Importance', fontsize=14, fontweight='bold')
    axes[1, 0].grid(True, alpha=0.3, axis='x')
    
    # 4. Error Distribution
    axes[1, 1].hist(residuals, bins=30, edgecolor='black', alpha=0.7, color='purple')
    axes[1, 1].axvline(x=0, color='r', linestyle='--', lw=2)
    axes[1, 1].set_xlabel('Prediction Error (weeks)', fontsize=12)
    axes[1, 1].set_ylabel('Frequency', fontsize=12)
    axes[1, 1].set_title('Error Distribution', fontsize=14, fontweight='bold')
    axes[1, 1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    plot_path = model_save_path / "training_results.png"
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"✅ Plots saved to {plot_path}")
    plt.close()

def save_model(model, scaler, feature_names, metrics):
    """Save trained model"""
    print("💾 Saving trained model...")
    
    model_data = {
        'model': model,
        'scaler': scaler,
        'feature_names': feature_names,
        'is_trained': True,
        'metrics': metrics
    }
    
    model_path = model_save_path / "timeline_model.pkl"
    with open(model_path, 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"✅ Model saved to {model_path}")

def main():
    """Main training pipeline"""
    
    # 1. Load data
    df = load_training_data()
    
    # 2. Prepare features
    X, y, feature_names = prepare_features_and_target(df)
    
    # 3. Split data
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=0.176, random_state=42
    )
    
    print(f"\n📊 Data split:")
    print(f"   Training:   {len(X_train)} samples ({len(X_train)/len(X)*100:.1f}%)")
    print(f"   Validation: {len(X_val)} samples ({len(X_val)/len(X)*100:.1f}%)")
    print(f"   Test:       {len(X_test)} samples ({len(X_test)/len(X)*100:.1f}%)\n")
    
    # 4. Scale features
    print("🔧 Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    print("✅ Features scaled\n")
    
    # 5. Train model
    model = train_model(X_train_scaled, y_train, X_val_scaled, y_val)
    
    # 6. Evaluate
    metrics, y_pred = evaluate_model(model, X_test_scaled, y_test)
    
    # 7. Visualize
    plot_results(y_test, y_pred, feature_names, model.feature_importances_)
    
    # 8. Save
    save_model(model, scaler, feature_names, metrics)
    
    print("\n" + "=" * 60)
    print("🎉 TRAINING COMPLETE!")
    print("=" * 60)
    print(f"✅ Model saved and ready for use")
    print(f"✅ Prediction accuracy: {metrics['within_2_weeks']:.1f}% within ±2 weeks")
    print(f"✅ R² Score: {metrics['r2_score']:.4f}")
    print("=" * 60)

if __name__ == "__main__":
    main()
