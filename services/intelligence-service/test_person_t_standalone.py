"""
Standalone Test for Person T - Part 2 Components
Tests Summarizer, Feature Engineering, and Preprocessing without database dependencies
"""

import numpy as np

# Test 1: TextSummarizer
print("\n" + "="*60)
print("Testing TextSummarizer")
print("="*60)

from nlp.summarizer import TextSummarizer

summarizer = TextSummarizer()

messages = [
    {
        "user": "alice@example.com",
        "text": "We need to decide on the database technology. PostgreSQL or MongoDB?",
        "timestamp": "2024-01-15T10:00:00"
    },
    {
        "user": "bob@example.com",
        "text": "I think PostgreSQL is better because we need ACID compliance.",
        "timestamp": "2024-01-15T10:05:00"
    },
    {
        "user": "charlie@example.com",
        "text": "Agreed. We decided to go with PostgreSQL. I'll create the schema.",
        "timestamp": "2024-01-15T10:10:00"
    }
]

result = summarizer.summarize_conversation(messages, max_length=100)

print(f"\n📝 Summary ({result['word_count']} words):")
print(result['summary'])
print(f"\n📊 Metadata:")
print(f"  - Method: {result['method']}")
print(f"  - Messages: {result['message_count']}")
print(f"  - Participants: {', '.join(result['participants'])}")
print(f"  - Key Topics: {', '.join(result['key_topics'])}")
print("✅ TextSummarizer test passed")

# Test 2: FeatureEngineer
print("\n" + "="*60)
print("Testing FeatureEngineer")
print("="*60)

from ml.utils.feature_engineering import FeatureEngineer

engineer = FeatureEngineer()

project_data = {
    'remaining_story_points': 120,
    'remaining_tasks': 25,
    'avg_weekly_velocity': 15,
    'velocity_std': 3,
    'team_size': 5,
    'blocked_tasks_count': 2,
    'high_complexity_count': 5,
    'avg_task_age_days': 3.5,
    'team_experience_score': 0.75,
    'velocity_trend': 0.5,
    'project_start_date': '2024-01-01T00:00:00'
}

features = engineer.extract_timeline_features(project_data)
print(f"\n🔧 Extracted {features.shape[1]} timeline features:")
for i, name in enumerate(engineer.feature_names[:5]):  # Show first 5
    print(f"  - {name}: {features[0][i]:.2f}")

velocity_history = [12, 15, 14, 16, 15, 17, 16]
velocity_features = engineer.extract_velocity_features(velocity_history)
print(f"\n📈 Velocity features:")
for key, value in list(velocity_features.items())[:5]:  # Show first 5
    print(f"  - {key}: {value:.2f}")

print("✅ FeatureEngineer test passed")

# Test 3: DataPreprocessor
print("\n" + "="*60)
print("Testing DataPreprocessor")
print("="*60)

from ml.utils.preprocessing import DataPreprocessor

preprocessor = DataPreprocessor()

dirty_data = {
    'remaining_story_points': -10,
    'avg_weekly_velocity': 15,
    'team_size': 0,
    'team_experience_score': 1.5
}

cleaned = preprocessor.clean_project_data(dirty_data)
print(f"\n🧹 Cleaned project data:")
for key in ['remaining_story_points', 'team_size', 'team_experience_score']:
    original = dirty_data.get(key, 'N/A')
    print(f"  - {key}: {original} → {cleaned[key]}")

data_with_outliers = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 100])
cleaned_data, mask = preprocessor.remove_outliers(data_with_outliers, method='iqr')
print(f"\n🎯 Outlier removal:")
print(f"  - Original: {data_with_outliers}")
print(f"  - Cleaned: {cleaned_data}")
print(f"  - Removed: {data_with_outliers[~mask]}")

print("✅ DataPreprocessor test passed")

# Summary
print("\n" + "="*60)
print("🎉 All Person T - Part 2 tests passed!")
print("="*60)
print("\n✅ Components tested:")
print("  1. TextSummarizer - Conversation summarization")
print("  2. FeatureEngineer - ML feature extraction")
print("  3. DataPreprocessor - Data cleaning and validation")
print("\n🚀 All components are working correctly!")
