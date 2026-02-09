"""
Test script for NLP components
Demonstrates DecisionExtractor, QuestionDetector, and EntityRecognizer
"""

from src.nlp import DecisionExtractor, QuestionDetector, EntityRecognizer
from loguru import logger

# Sample conversation data
sample_messages = [
    {
        'user': 'alice@example.com',
        'text': 'Should we use PostgreSQL or MongoDB for the new project?',
        'timestamp': '2024-01-15T10:00:00'
    },
    {
        'user': 'bob@example.com',
        'text': 'We decided to go with PostgreSQL because it has better ACID compliance and our team has more experience with it.',
        'timestamp': '2024-01-15T10:05:00'
    },
    {
        'user': 'charlie@example.com',
        'text': '@alice can you review PR-123? It implements the FastAPI authentication module.',
        'timestamp': '2024-01-15T10:10:00'
    },
    {
        'user': 'alice@example.com',
        'text': 'Sure! How urgent is this? I have a blocker on PROJ-456.',
        'timestamp': '2024-01-15T10:15:00'
    },
    {
        'user': 'charlie@example.com',
        'text': 'Not urgent, but would be great to get it in before the sprint ends.',
        'timestamp': '2024-01-15T10:20:00'
    },
    {
        'user': 'bob@example.com',
        'text': 'Let\'s also use React for the frontend and integrate with our existing Django backend.',
        'timestamp': '2024-01-15T10:25:00'
    }
]


def test_decision_extractor():
    """Test DecisionExtractor"""
    logger.info("=" * 60)
    logger.info("Testing DecisionExtractor")
    logger.info("=" * 60)
    
    extractor = DecisionExtractor()
    decisions = extractor.extract_decisions(sample_messages, min_confidence=0.5)
    
    print(f"\n📊 Found {len(decisions)} decisions:\n")
    for i, decision in enumerate(decisions, 1):
        print(f"{i}. {decision['decision']}")
        print(f"   - Type: {decision['type']}")
        print(f"   - Decided by: {decision['decided_by']}")
        print(f"   - Confidence: {decision['confidence']:.0%}")
        if decision.get('rationale'):
            print(f"   - Rationale: {decision['rationale']}")
        print()
    
    # Generate summary
    summary = extractor.summarize_decisions(decisions)
    print("\n" + summary)
    print()


def test_question_detector():
    """Test QuestionDetector"""
    logger.info("=" * 60)
    logger.info("Testing QuestionDetector")
    logger.info("=" * 60)
    
    detector = QuestionDetector()
    questions = detector.detect_questions(sample_messages, min_confidence=0.5)
    
    print(f"\n❓ Found {len(questions)} questions:\n")
    for i, question in enumerate(questions, 1):
        print(f"{i}. {question['question']}")
        print(f"   - Type: {question['type']}")
        print(f"   - Urgency: {question['urgency']}")
        print(f"   - Asked by: {question['asker']}")
        print(f"   - Answered: {'Yes' if question['is_answered'] else 'No'}")
        if question['is_answered']:
            print(f"   - Answered by: {question['answered_by']}")
        print()
    
    # Find unanswered
    unanswered = detector.find_unanswered_questions(questions, max_age_hours=24)
    print(f"\n⚠️  {len(unanswered)} unanswered questions")
    
    # Generate summary
    summary = detector.summarize_questions(questions)
    print("\n" + summary)
    print()


def test_entity_recognizer():
    """Test EntityRecognizer"""
    logger.info("=" * 60)
    logger.info("Testing EntityRecognizer")
    logger.info("=" * 60)
    
    recognizer = EntityRecognizer()
    
    # Extract entities from all messages
    all_entities = {
        'people': [],
        'tasks': [],
        'technologies': []
    }
    
    for msg in sample_messages:
        entities = recognizer.extract_entities(msg['text'])
        all_entities['people'].extend(entities.get('people', []))
        all_entities['tasks'].extend(entities.get('tasks', []))
        all_entities['technologies'].extend(entities.get('technologies', []))
    
    print(f"\n🔍 Extracted entities:\n")
    print(f"People mentioned: {len(all_entities['people'])}")
    for person in all_entities['people']:
        print(f"  - {person['text']} ({person['type']})")
    
    print(f"\nTasks mentioned: {len(all_entities['tasks'])}")
    for task in all_entities['tasks']:
        print(f"  - {task['text']} ({task['type']})")
    
    print(f"\nTechnologies mentioned: {len(all_entities['technologies'])}")
    for tech in all_entities['technologies']:
        print(f"  - {tech['text']} ({tech.get('category', 'unknown')})")
    
    # Extract relationships
    relationships = recognizer.extract_relationships(sample_messages)
    print(f"\n🔗 Relationships:")
    print(f"  - Person-Task: {len(relationships['person_task'])}")
    print(f"  - Person-Technology: {len(relationships['person_technology'])}")
    print(f"  - Person-Person: {len(relationships['person_person'])}")
    
    # Generate summary
    summary = recognizer.summarize_entities(sample_messages)
    print("\n" + summary)
    print()


def main():
    """Run all tests"""
    logger.info("🚀 Starting NLP Components Test\n")
    
    test_decision_extractor()
    test_question_detector()
    test_entity_recognizer()
    
    logger.success("✅ All NLP components tested successfully!")


if __name__ == "__main__":
    main()
