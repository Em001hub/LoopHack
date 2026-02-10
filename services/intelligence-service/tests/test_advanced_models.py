"""
Test Advanced ML Models
Tests for SkillExtractor, SentimentAnalyzer, ConversationParser, and MonteCarloSimulator
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from ml.models.skill_extractor import SkillExtractor
from ml.models.sentiment_analyzer import SentimentAnalyzer
from nlp.conversation_parser import ConversationParser
from simulation.monte_carlo import MonteCarloSimulator


class TestSkillExtractor:
    """Test SkillExtractor model"""
    
    def test_initialization(self):
        """Test SkillExtractor initializes correctly"""
        extractor = SkillExtractor()
        assert extractor is not None
        assert 'languages' in extractor.tech_vocabulary
        assert 'frameworks' in extractor.tech_vocabulary
    
    def test_technical_term_detection(self):
        """Test detecting technical terms in text"""
        extractor = SkillExtractor()
        
        text = "I'm working with Python and React to build a FastAPI backend"
        terms = extractor._detect_technical_terms(text)
        
        assert 'python' in terms
        assert 'react' in terms
        assert 'fastapi' in terms
    
    def test_github_skill_extraction(self):
        """Test extracting skills from GitHub events"""
        extractor = SkillExtractor()
        
        github_events = [
            {
                'timestamp': datetime.now().isoformat(),
                'metadata': {
                    'languages': {'Python': 500, 'JavaScript': 200},
                    'technical_areas': ['backend', 'api design'],
                    'message': 'Implemented FastAPI endpoint'
                }
            },
            {
                'timestamp': (datetime.now() - timedelta(days=10)).isoformat(),
                'metadata': {
                    'languages': {'Python': 300},
                    'technical_areas': ['testing'],
                    'message': 'Added pytest tests'
                }
            }
        ]
        
        skills = extractor.extract_skills_from_github('user_123', github_events)
        
        assert 'languages' in skills
        assert 'frameworks' in skills
        assert 'technical_areas' in skills
        assert len(skills['languages']) > 0
    
    def test_slack_expertise_extraction(self):
        """Test extracting expertise from Slack messages"""
        extractor = SkillExtractor()
        
        slack_messages = [
            {
                'metadata': {
                    'text': 'You can use React hooks for this problem',
                    'intent': 'help_offer'
                }
            },
            {
                'metadata': {
                    'text': 'How do I configure Docker?',
                    'intent': 'question'
                }
            }
        ]
        
        skills = extractor.extract_skills_from_slack('user_123', slack_messages)
        
        assert 'slack_expertise' in skills
        assert len(skills['slack_expertise']) > 0
    
    def test_task_matching(self):
        """Test matching user skills to task requirements"""
        extractor = SkillExtractor()
        
        user_skills = {
            'technical_skills': [
                {'name': 'Python', 'proficiency': 0.9},
                {'name': 'React', 'proficiency': 0.7}
            ],
            'confidence': 0.85
        }
        
        task_requirements = {
            'required_skills': ['Python', 'FastAPI'],
            'preferred_skills': ['React', 'Docker']
        }
        
        match = extractor.recommend_task_match(user_skills, task_requirements)
        
        assert 'match_score' in match
        assert 'recommendation' in match
        assert match['match_score'] >= 0 and match['match_score'] <= 1


class TestSentimentAnalyzer:
    """Test SentimentAnalyzer model"""
    
    def test_initialization(self):
        """Test SentimentAnalyzer initializes correctly"""
        analyzer = SentimentAnalyzer()
        assert analyzer is not None
        assert 'frustration' in analyzer.emotion_keywords
    
    def test_positive_sentiment(self):
        """Test analyzing positive message"""
        analyzer = SentimentAnalyzer()
        
        result = analyzer.analyze_message("This is great work! I'm really happy with the progress.")
        
        assert result['label'] in ['positive', 'neutral', 'negative']
        assert result['score'] >= -1 and result['score'] <= 1
        assert 'confidence' in result
    
    def test_negative_sentiment(self):
        """Test analyzing negative message"""
        analyzer = SentimentAnalyzer()
        
        result = analyzer.analyze_message("I'm frustrated and stuck on this problem. It's terrible.")
        
        assert result['label'] in ['positive', 'neutral', 'negative']
        assert 'frustration' in result['emotions'] or result['label'] == 'negative'
    
    def test_emotion_detection(self):
        """Test detecting specific emotions"""
        analyzer = SentimentAnalyzer()
        
        emotions = analyzer._detect_emotions("I'm stressed and overwhelmed with this deadline")
        
        assert 'stress' in emotions
    
    def test_sentiment_trend_analysis(self):
        """Test analyzing sentiment trend over time"""
        analyzer = SentimentAnalyzer()
        
        messages = [
            {
                'timestamp': (datetime.now() - timedelta(days=i)).isoformat(),
                'text': 'Great progress today!' if i < 5 else 'Frustrated with blockers'
            }
            for i in range(10)
        ]
        
        trend = analyzer.analyze_user_sentiment_trend('user_123', messages)
        
        if trend.get('status') != 'insufficient_data':
            assert 'sentiment_trend' in trend
            assert 'current_sentiment' in trend
            assert 'burnout_risk' in trend
    
    def test_burnout_risk_calculation(self):
        """Test burnout risk detection"""
        analyzer = SentimentAnalyzer()
        
        # Simulated declining sentiment
        data = {
            'sentiment_trend': -0.05,  # Declining
            'recent_sentiment': -0.4,  # Negative
            'overall_sentiment': -0.3,
            'messages': [
                {'text': 'I am frustrated and stuck'},
                {'text': 'Feeling overwhelmed and stressed'}
            ]
        }
        
        risk = analyzer._calculate_burnout_risk(data)
        
        assert 'score' in risk
        assert 'level' in risk
        assert risk['level'] in ['Low', 'Medium', 'High']


class TestConversationParser:
    """Test ConversationParser"""
    
    def test_initialization(self):
        """Test ConversationParser initializes"""
        parser = ConversationParser()
        assert parser is not None
    
    def test_fallback_parsing(self):
        """Test fallback parsing when GPT-4 unavailable"""
        parser = ConversationParser()
        
        messages = [
            {
                'user_id': 'alice@example.com',
                'text': 'We are blocked on the API integration',
                'timestamp': datetime.now().isoformat()
            },
            {
                'user_id': 'bob@example.com',
                'text': 'I will work on fixing it tomorrow',
                'timestamp': datetime.now().isoformat()
            }
        ]
        
        result = parser._fallback_parsing(messages)
        
        assert 'topic' in result
        assert 'blockers' in result
        assert 'action_items' in result
    
    def test_conversation_formatting(self):
        """Test formatting messages for parsing"""
        parser = ConversationParser()
        
        messages = [
            {
                'user_email': 'alice@example.com',
                'text': 'Hello team',
                'timestamp': '2024-01-01T10:00:00Z'
            }
        ]
        
        formatted = parser._format_conversation(messages)
        
        assert 'alice@example.com' in formatted
        assert 'Hello team' in formatted
    
    def test_summary_generation(self):
        """Test generating summary from analysis"""
        parser = ConversationParser()
        
        analysis = {
            'topic': 'API Integration Discussion',
            'decisions': [{'decision': 'Use REST API'}],
            'action_items': [{'action': 'Implement endpoint', 'owner': 'Alice'}],
            'blockers': [{'blocker': 'Missing credentials'}]
        }
        
        summary = parser.generate_summary(analysis)
        
        assert 'API Integration' in summary
        assert 'Decisions' in summary or 'decisions' in summary.lower()


class TestMonteCarloSimulator:
    """Test MonteCarloSimulator"""
    
    def test_initialization(self):
        """Test simulator initializes correctly"""
        simulator = MonteCarloSimulator(n_simulations=100)
        assert simulator.n_simulations == 100
    
    def test_single_simulation(self):
        """Test running a single simulation"""
        simulator = MonteCarloSimulator(n_simulations=10)
        
        weeks, blockers = simulator._run_single_simulation(
            remaining_points=100,
            avg_velocity=20,
            velocity_std=3,
            team_size=5
        )
        
        assert weeks > 0
        assert weeks < 104  # Max 2 years
        assert blockers >= 0
    
    def test_project_timeline_simulation(self):
        """Test full project timeline simulation"""
        simulator = MonteCarloSimulator(n_simulations=100)
        
        project_data = {
            'remaining_story_points': 100,
            'avg_weekly_velocity': 20,
            'velocity_std': 3,
            'team_size': 5
        }
        
        result = simulator.simulate_project_timeline(project_data)
        
        assert 'simulation_count' in result
        assert 'predicted_weeks' in result
        assert 'percentiles' in result
        assert 'p10' in result['percentiles']
        assert 'p50' in result['percentiles']
        assert 'p90' in result['percentiles']
    
    def test_scenario_application(self):
        """Test applying what-if scenarios"""
        simulator = MonteCarloSimulator(n_simulations=10)
        
        scenario = {
            'add_developers': 2,
            'reduce_scope_pct': 10
        }
        
        remaining, velocity, std, team_size = simulator._apply_scenario(
            remaining_points=100,
            avg_velocity=20,
            velocity_std=3,
            team_size=5,
            scenario_params=scenario
        )
        
        # Team size should increase
        assert team_size == 7
        
        # Scope should decrease
        assert remaining < 100
    
    def test_histogram_creation(self):
        """Test creating histogram data"""
        simulator = MonteCarloSimulator()
        
        import numpy as np
        data = np.random.normal(10, 2, 100)
        
        histogram = simulator._create_histogram(data, bins=10)
        
        assert 'bins' in histogram
        assert 'counts' in histogram
        assert len(histogram['bins']) == 10
    
    def test_scenario_comparison(self):
        """Test comparing multiple scenarios"""
        simulator = MonteCarloSimulator(n_simulations=50)
        
        project_data = {
            'remaining_story_points': 100,
            'avg_weekly_velocity': 20,
            'team_size': 5
        }
        
        scenarios = [
            {'name': 'Add 2 devs', 'add_developers': 2},
            {'name': 'Reduce scope 20%', 'reduce_scope_pct': 20}
        ]
        
        comparison = simulator.compare_scenarios(project_data, scenarios)
        
        assert 'scenarios' in comparison
        assert 'baseline' in comparison['scenarios']
        assert 'comparison_table' in comparison
        assert 'recommendation' in comparison


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
