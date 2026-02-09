"""
Test Person T - Part 2 Components
Tests for Summarizer, Feature Engineering, and Preprocessing
"""

import sys
sys.path.insert(0, 'src')

from nlp.summarizer import TextSummarizer
from ml.utils.feature_engineering import FeatureEngineer
from ml.utils.preprocessing import DataPreprocessor
import numpy as np

def test_summarizer():
    """Test TextSummarizer"""
    print("\n" + "="*60)
    print("Testing TextSummarizer")
    print("="*60)
    
    summarizer = TextSummarizer()
    
    # Sample messages
    messages = [
        {
            "user": "alice@example.com",
            "text": "We need to decide on the database technology for the new project. PostgreSQL or MongoDB?",
            "timestamp": "2024-01-15T10:00:00"
        },
        {
            "user": "bob@example.com",
            "text": "I think PostgreSQL is better for our use case because we need ACID compliance and our team has more experience with it.",
            "timestamp": "2024-01-15T10:05:00"
        },
        {
            "user": "charlie@example.com",
            "text": "Agreed. We decided to go with PostgreSQL. I'll create the initial schema and migration scripts.",
            "timestamp": "2024-01-15T10:10:00"
        },
        {
            "user": "alice@example.com",
            "text": "Great! Can you also set up the connection pooling and implement the repository pattern?",
            "timestamp": "2024-01-15T10:15:00"
        }
    ]
    
    # Test summarization
    result = summarizer.summarize_conversation(messages, max_length=100)
    
    print(f"\n📝 Summary ({result['word_count']} words):")
    print(result['summary'])
    print(f"\n📊 Metadata:")
    print(f"  - Method: {result['method']}")
    print(f"  - Messages: {result['message_count']}")
    print(f"  - Participants: {', '.join(result['participants'])}")
    print(f"  - Key Topics: {', '.join(result['key_topics'])}")
    
    print("✅ TextSummarizer test passed")


def test_feature_engineer():
    """Test FeatureEngineer"""
    print("\n" + "="*60)
    print("Testing FeatureEngineer")
    print("="*60)
    
    engineer = FeatureEngineer()
    
    # Sample project data
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
    
    # Extract timeline features
    features = engineer.extract_timeline_features(project_data)
    print(f"\n🔧 Extracted {features.shape[1]} timeline features:")
    for i, name in enumerate(engineer.feature_names):
        print(f"  - {name}: {features[0][i]:.2f}")
    
    # Test velocity features
    velocity_history = [12, 15, 14, 16, 15, 17, 16]
    velocity_features = engineer.extract_velocity_features(velocity_history)
    print(f"\n📈 Velocity features:")
    for key, value in velocity_features.items():
        print(f"  - {key}: {value:.2f}")
    
    # Test team features
    team_data = [
        {'experience_score': 0.8, 'seniority': 'senior', 'skills': ['python', 'react', 'aws']},
        {'experience_score': 0.6, 'seniority': 'mid', 'skills': ['python', 'django']},
        {'experience_score': 0.4, 'seniority': 'junior', 'skills': ['react', 'javascript']},
    ]
    team_features = engineer.extract_team_features(team_data)
    print(f"\n👥 Team features:")
    for key, value in team_features.items():
        print(f"  - {key}: {value}")
    
    print("✅ FeatureEngineer test passed")


def test_preprocessor():
    """Test DataPreprocessor"""
    print("\n" + "="*60)
    print("Testing DataPreprocessor")
    print("="*60)
    
    preprocessor = DataPreprocessor()
    
    # Test clean_project_data
    dirty_data = {
        'remaining_story_points': -10,  # Negative (should be fixed)
        'avg_weekly_velocity': 15,
        'team_size': 0,  # Invalid (should be 1)
        'team_experience_score': 1.5  # Out of range (should be 1.0)
    }
    
    cleaned = preprocessor.clean_project_data(dirty_data)
    print(f"\n🧹 Cleaned project data:")
    for key, value in cleaned.items():
        original = dirty_data.get(key, 'N/A')
        print(f"  - {key}: {original} → {value}")
    
    # Test outlier removal
    data_with_outliers = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 100])  # 100 is outlier
    cleaned_data, mask = preprocessor.remove_outliers(data_with_outliers, method='iqr')
    print(f"\n🎯 Outlier removal:")
    print(f"  - Original: {data_with_outliers}")
    print(f"  - Cleaned: {cleaned_data}")
    print(f"  - Removed: {data_with_outliers[~mask]}")
    
    # Test velocity validation
    invalid_velocity = [-5, 0, 15, 20, 1500, 18]  # Has invalid values
    valid_velocity = preprocessor.validate_velocity_history(invalid_velocity)
    print(f"\n📊 Velocity validation:")
    print(f"  - Original: {invalid_velocity}")
    print(f"  - Valid: {valid_velocity}")
    
    # Test normalization
    features = np.array([[1, 10, 100], [2, 20, 200], [3, 30, 300]])
    normalized = preprocessor.normalize_features(features, method='standard')
    print(f"\n📏 Feature normalization (standard):")
    print(f"  - Original:\n{features}")
    print(f"  - Normalized:\n{normalized}")
    
    print("✅ DataPreprocessor test passed")


def main():
    """Run all tests"""
    print("🚀 Starting Person T - Part 2 Tests\n")
    
    try:
        test_summarizer()
        test_feature_engineer()
        test_preprocessor()
        
        print("\n" + "="*60)
        print("🎉 All Person T - Part 2 tests passed!")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise


if __name__ == "__main__":
    main()
