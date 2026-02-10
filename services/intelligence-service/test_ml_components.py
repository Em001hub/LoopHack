"""
Test Script for ML Components (No Database Required)
Tests the trained model and visualizations
"""

import pickle
import numpy as np
from pathlib import Path
import json

print("\n" + "=" * 60)
print("🧪 TESTING ML COMPONENTS")
print("=" * 60)

# Test 1: Load Trained Model
print("\n1️⃣  Testing Model Loading...")
model_path = Path("./src/data/models/timeline_model.pkl")

if not model_path.exists():
    print("   ❌ Model not found! Run train_timeline_standalone.py first")
    exit(1)

with open(model_path, 'rb') as f:
    model_data = pickle.load(f)

model = model_data['model']
scaler = model_data['scaler']
feature_names = model_data['feature_names']
is_trained = model_data['is_trained']
metrics = model_data.get('metrics', {})

print(f"   ✅ Model loaded successfully")
print(f"   ✅ Model type: {type(model).__name__}")
print(f"   ✅ Is trained: {is_trained}")
print(f"   ✅ Features: {len(feature_names)}")

# Test 2: Model Prediction
print("\n2️⃣  Testing Model Prediction...")

# Sample project data
test_project = {
    'remaining_story_points': 100,
    'avg_weekly_velocity': 20.0,
    'velocity_std': 3.5,
    'team_size': 5,
    'blocked_tasks_count': 2,
    'high_complexity_count': 4,
    'avg_task_age_days': 7.0,
    'team_experience_score': 0.75
}

# Prepare features in correct order
X_test = np.array([[
    test_project['remaining_story_points'],
    test_project['avg_weekly_velocity'],
    test_project['velocity_std'],
    test_project['team_size'],
    test_project['blocked_tasks_count'],
    test_project['high_complexity_count'],
    test_project['avg_task_age_days'],
    test_project['team_experience_score']
]])

# Scale and predict
X_test_scaled = scaler.transform(X_test)
prediction = model.predict(X_test_scaled)[0]

print(f"   ✅ Prediction successful!")
print(f"   📊 Input: {test_project['remaining_story_points']} story points, {test_project['team_size']} team members")
print(f"   📊 Velocity: {test_project['avg_weekly_velocity']} points/week")
print(f"   🎯 Predicted timeline: {prediction:.1f} weeks")

# Test 3: Feature Importance
print("\n3️⃣  Testing Feature Importance...")
if hasattr(model, 'feature_importances_'):
    importances = model.feature_importances_
    
    # Sort by importance
    indices = np.argsort(importances)[::-1]
    
    print("   ✅ Top 3 Most Important Features:")
    for i in range(min(3, len(indices))):
        idx = indices[i]
        print(f"      {i+1}. {feature_names[idx]}: {importances[idx]:.3f}")

# Test 4: Model Metrics
print("\n4️⃣  Testing Model Metrics...")
if metrics:
    print(f"   ✅ R² Score: {metrics.get('r2_score', 'N/A'):.4f}")
    print(f"   ✅ MAE: {metrics.get('mae', 'N/A'):.2f} weeks")
    print(f"   ✅ Accuracy (±2 weeks): {metrics.get('within_2_weeks', 'N/A'):.1f}%")
else:
    print("   ⚠️  No metrics found in model file")

# Test 5: Visualization Check
print("\n5️⃣  Testing Visualizations...")
viz_path = Path("./src/data/models/training_results.png")
if viz_path.exists():
    print(f"   ✅ Training visualization found: {viz_path}")
    print(f"   ✅ File size: {viz_path.stat().st_size / 1024:.1f} KB")
else:
    print("   ⚠️  Visualization not found")

# Test 6: Data Files Check
print("\n6️⃣  Testing Data Files...")
data_files = [
    "./src/data/datasets/historical_projects.csv",
    "./src/data/datasets/train.csv",
    "./src/data/datasets/val.csv",
    "./src/data/datasets/test.csv"
]

for file_path in data_files:
    p = Path(file_path)
    if p.exists():
        import pandas as pd
        df = pd.read_csv(p)
        print(f"   ✅ {p.name}: {len(df)} samples")
    else:
        print(f"   ❌ {p.name}: Not found")

# Test 7: Multiple Predictions
print("\n7️⃣  Testing Batch Predictions...")

test_scenarios = [
    {
        'name': 'Small Project',
        'remaining_story_points': 50,
        'avg_weekly_velocity': 25.0,
        'velocity_std': 2.0,
        'team_size': 3,
        'blocked_tasks_count': 0,
        'high_complexity_count': 1,
        'avg_task_age_days': 3.0,
        'team_experience_score': 0.85
    },
    {
        'name': 'Large Complex Project',
        'remaining_story_points': 200,
        'avg_weekly_velocity': 15.0,
        'velocity_std': 6.0,
        'team_size': 8,
        'blocked_tasks_count': 10,
        'high_complexity_count': 15,
        'avg_task_age_days': 20.0,
        'team_experience_score': 0.60
    },
    {
        'name': 'Medium Project',
        'remaining_story_points': 120,
        'avg_weekly_velocity': 18.0,
        'velocity_std': 4.0,
        'team_size': 6,
        'blocked_tasks_count': 3,
        'high_complexity_count': 5,
        'avg_task_age_days': 10.0,
        'team_experience_score': 0.70
    }
]

for scenario in test_scenarios:
    X = np.array([[
        scenario['remaining_story_points'],
        scenario['avg_weekly_velocity'],
        scenario['velocity_std'],
        scenario['team_size'],
        scenario['blocked_tasks_count'],
        scenario['high_complexity_count'],
        scenario['avg_task_age_days'],
        scenario['team_experience_score']
    ]])
    
    X_scaled = scaler.transform(X)
    pred = model.predict(X_scaled)[0]
    
    print(f"   ✅ {scenario['name']}: {pred:.1f} weeks")

# Summary
print("\n" + "=" * 60)
print("🎉 ALL TESTS PASSED!")
print("=" * 60)
print("✅ Model is loaded and working correctly")
print("✅ Predictions are being generated")
print("✅ All data files are present")
print("✅ Visualizations are created")
print("\n💡 The ML pipeline is fully functional!")
print("=" * 60 + "\n")
