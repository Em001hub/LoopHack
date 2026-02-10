"""
Standalone Data Preparation Script (No Database Required)
Generates synthetic training data for ML models
"""

import numpy as np
import pandas as pd
from pathlib import Path
import json
from sklearn.model_selection import train_test_split

print("📊 Starting Data Preparation (Standalone Mode)")
print("=" * 60)

# Set random seed for reproducibility
np.random.seed(42)

# Output directory
output_dir = Path("./src/data/datasets")
output_dir.mkdir(parents=True, exist_ok=True)

def load_mock_data():
    """Load mock data from JSON if available"""
    mock_file = output_dir / "mock_projects.json"
    
    if mock_file.exists():
        print(f"✅ Loading mock data from {mock_file}")
        with open(mock_file, 'r') as f:
            data = json.load(f)
        return pd.DataFrame(data)
    else:
        print("⚠️  No mock data found, will generate synthetic data")
        return None

def generate_synthetic_data(n_samples=100):
    """Generate synthetic training data"""
    print(f"🎲 Generating {n_samples} synthetic training samples...")
    
    data = []
    
    for i in range(n_samples):
        # Random project parameters
        team_size = np.random.randint(2, 12)
        remaining_points = np.random.randint(20, 250)
        velocity = np.random.uniform(8, 35)
        velocity_std = velocity * np.random.uniform(0.1, 0.5)
        blocked_tasks = np.random.randint(0, 12)
        high_complexity = np.random.randint(0, 10)
        avg_task_age = np.random.uniform(0, 30)
        team_experience = np.random.uniform(0.3, 0.95)
        
        # Calculate actual weeks (with realistic variance)
        base_weeks = remaining_points / velocity
        risk_multiplier = 1.0 + (blocked_tasks * 0.08) + (high_complexity * 0.05)
        actual_weeks = base_weeks * risk_multiplier * np.random.uniform(0.85, 1.15)
        
        # Ensure reasonable bounds
        actual_weeks = max(1.0, min(actual_weeks, 52.0))
        
        data.append({
            'project_id': f'synthetic_{i:03d}',
            'project_name': f'Project {i}',
            'remaining_story_points': remaining_points,
            'avg_weekly_velocity': velocity,
            'velocity_std': velocity_std,
            'team_size': team_size,
            'blocked_tasks_count': blocked_tasks,
            'high_complexity_count': high_complexity,
            'avg_task_age_days': avg_task_age,
            'team_experience_score': team_experience,
            'actual_weeks_taken': actual_weeks
        })
    
    print(f"✅ Generated {n_samples} synthetic samples")
    return pd.DataFrame(data)

def clean_data(df):
    """Clean and validate dataset"""
    print("🧹 Cleaning dataset...")
    
    # Remove outliers (projects > 52 weeks or < 1 week)
    initial_count = len(df)
    df = df[(df['actual_weeks_taken'] >= 1) & (df['actual_weeks_taken'] <= 52)]
    removed = initial_count - len(df)
    
    if removed > 0:
        print(f"   Removed {removed} outliers")
    
    # Ensure no negative values
    numeric_cols = [
        'remaining_story_points', 'avg_weekly_velocity', 'velocity_std',
        'team_size', 'blocked_tasks_count', 'high_complexity_count',
        'avg_task_age_days'
    ]
    
    for col in numeric_cols:
        df[col] = df[col].clip(lower=0)
    
    # Ensure team_size >= 1
    df['team_size'] = df['team_size'].clip(lower=1)
    
    # Ensure velocity > 0
    df['avg_weekly_velocity'] = df['avg_weekly_velocity'].clip(lower=0.1)
    
    print(f"✅ Dataset cleaned: {len(df)} samples")
    
    return df

def main():
    """Main data preparation function"""
    
    # Try to load mock data first
    df = load_mock_data()
    
    # If no mock data or insufficient, generate synthetic
    if df is None or len(df) < 10:
        synthetic_df = generate_synthetic_data(100)
        
        if df is not None:
            print("📈 Augmenting mock data with synthetic data...")
            df = pd.concat([df, synthetic_df], ignore_index=True)
        else:
            df = synthetic_df
    
    # Clean data
    df = clean_data(df)
    
    # Print statistics
    print("\n📊 DATASET STATISTICS:")
    print("=" * 60)
    print(df.describe().to_string())
    print("=" * 60)
    
    # Save full dataset
    output_path = output_dir / "historical_projects.csv"
    df.to_csv(output_path, index=False)
    print(f"\n✅ Training data saved to {output_path}")
    
    # Split into train/val/test
    train_df, test_df = train_test_split(df, test_size=0.15, random_state=42)
    train_df, val_df = train_test_split(train_df, test_size=0.176, random_state=42)
    
    train_df.to_csv(output_dir / "train.csv", index=False)
    val_df.to_csv(output_dir / "val.csv", index=False)
    test_df.to_csv(output_dir / "test.csv", index=False)
    
    print(f"\n✅ Split datasets saved:")
    print(f"   - Train: {len(train_df)} samples ({len(train_df)/len(df)*100:.1f}%)")
    print(f"   - Val:   {len(val_df)} samples ({len(val_df)/len(df)*100:.1f}%)")
    print(f"   - Test:  {len(test_df)} samples ({len(test_df)/len(df)*100:.1f}%)")
    
    print("\n" + "=" * 60)
    print("🎉 DATA PREPARATION COMPLETE!")
    print("=" * 60)
    print("Next step: Run train_timeline_standalone.py to train the model")
    print("=" * 60)

if __name__ == "__main__":
    main()
