"""
Simple test script to verify the Intelligence Service is working
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

print("🧪 Testing Intelligence Service Components\n")
print("=" * 50)

# Test 1: Import Timeline Predictor
print("\n1️⃣ Testing Timeline Predictor Import...")
try:
    from ml.models.timeline_predictor import TimelinePredictor
    print("   ✅ TimelinePredictor imported successfully")
except Exception as e:
    print(f"   ❌ Failed to import: {e}")
    sys.exit(1)

# Test 2: Create Predictor Instance
print("\n2️⃣ Creating Predictor Instance...")
try:
    predictor = TimelinePredictor()
    print(f"   ✅ Predictor created (trained: {predictor.is_trained})")
    print(f"   ✅ Features: {len(predictor.feature_names)}")
except Exception as e:
    print(f"   ❌ Failed to create predictor: {e}")
    sys.exit(1)

# Test 3: Test Heuristic Prediction
print("\n3️⃣ Testing Heuristic Prediction...")
try:
    sample_data = {
        'remaining_story_points': 100,
        'avg_weekly_velocity': 20,
        'velocity_std': 3,
        'team_size': 5,
        'blocked_tasks_count': 2,
        'high_complexity_count': 5,
        'avg_task_age_days': 7,
        'team_experience_score': 0.75
    }
    
    result = predictor.predict_completion_date(sample_data)
    
    print(f"   ✅ Prediction successful!")
    print(f"   📅 Predicted completion: {result['predicted_completion_date'][:10]}")
    print(f"   ⏱️  Weeks remaining: {result['predicted_weeks_remaining']:.1f}")
    print(f"   🎯 Confidence: {result['model_confidence'] * 100:.0f}%")
    print(f"   ⚠️  Risk factors: {len(result['risk_factors'])}")
    
    for risk in result['risk_factors']:
        print(f"      - {risk}")
        
except Exception as e:
    print(f"   ❌ Prediction failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Test Feature Extraction
print("\n4️⃣ Testing Feature Extraction...")
try:
    features = predictor.extract_features(sample_data)
    print(f"   ✅ Features extracted: shape {features.shape}")
    print(f"   ✅ Feature values: {features[0][:3]}...")
except Exception as e:
    print(f"   ❌ Feature extraction failed: {e}")
    sys.exit(1)

# Test 5: Import FastAPI App
print("\n5️⃣ Testing FastAPI App Import...")
try:
    from main import app
    print(f"   ✅ FastAPI app imported")
    print(f"   ✅ App title: {app.title}")
except Exception as e:
    print(f"   ❌ Failed to import app: {e}")
    sys.exit(1)

print("\n" + "=" * 50)
print("✅ All tests passed! Intelligence Service is working correctly.")
print("\n📝 Next steps:")
print("   1. Run: python -m uvicorn src.main:app --reload --port 4002")
print("   2. Open: http://localhost:4002/docs")
print("   3. Open: demo.html in your browser")
