"""
Conversation Intelligence Endpoints
Analyze conversations for decisions, questions, and entities
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from loguru import logger

from src.nlp import DecisionExtractor, QuestionDetector, EntityRecognizer

router = APIRouter(prefix="/conversation", tags=["Conversation Intelligence"])

# Initialize NLP components
decision_extractor = DecisionExtractor()
question_detector = QuestionDetector()
entity_recognizer = EntityRecognizer()


class Message(BaseModel):
    """Single message in conversation"""
    user: str
    text: str
    timestamp: str
    user_email: Optional[str] = None
    thread_ts: Optional[str] = None


class ConversationRequest(BaseModel):
    """Request to analyze conversation"""
    messages: List[Message]
    min_confidence: Optional[float] = 0.6


class DecisionResponse(BaseModel):
    """Decision extraction response"""
    decisions: List[Dict]
    total_count: int
    by_type: Dict[str, int]
    summary: str


class QuestionResponse(BaseModel):
    """Question detection response"""
    questions: List[Dict]
    total_count: int
    unanswered_count: int
    alerts: List[Dict]
    summary: str


class EntityResponse(BaseModel):
    """Entity recognition response"""
    entities: Dict[str, List[Dict]]
    relationships: Dict[str, List[Dict]]
    most_mentioned: Dict[str, List[tuple]]
    summary: str


@router.post("/analyze-decisions", response_model=DecisionResponse)
async def analyze_decisions(request: ConversationRequest):
    """
    Extract decisions from conversation
    
    **Returns:**
    - List of decisions with metadata
    - Breakdown by decision type
    - Summary text
    """
    try:
        logger.info(f"Analyzing {len(request.messages)} messages for decisions")
        
        # Convert to dict format
        messages = [msg.dict() for msg in request.messages]
        
        # Extract decisions
        decisions = decision_extractor.extract_decisions(
            messages,
            min_confidence=request.min_confidence
        )
        
        # Group by type
        by_type = {}
        for decision in decisions:
            decision_type = decision.get('type', 'general')
            by_type[decision_type] = by_type.get(decision_type, 0) + 1
        
        # Generate summary
        summary = decision_extractor.summarize_decisions(decisions)
        
        return DecisionResponse(
            decisions=decisions,
            total_count=len(decisions),
            by_type=by_type,
            summary=summary
        )
        
    except Exception as e:
        logger.error(f"Error analyzing decisions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-questions", response_model=QuestionResponse)
async def analyze_questions(request: ConversationRequest):
    """
    Detect questions and identify unanswered ones
    
    **Returns:**
    - List of questions with metadata
    - Unanswered questions
    - Alerts for urgent unanswered questions
    - Summary text
    """
    try:
        logger.info(f"Analyzing {len(request.messages)} messages for questions")
        
        # Convert to dict format
        messages = [msg.dict() for msg in request.messages]
        
        # Detect questions
        questions = question_detector.detect_questions(
            messages,
            min_confidence=request.min_confidence
        )
        
        # Find unanswered
        unanswered = question_detector.find_unanswered_questions(
            questions,
            max_age_hours=24
        )
        
        # Generate alerts
        alerts = question_detector.generate_alerts(unanswered)
        
        # Generate summary
        summary = question_detector.summarize_questions(questions)
        
        return QuestionResponse(
            questions=questions,
            total_count=len(questions),
            unanswered_count=len(unanswered),
            alerts=alerts,
            summary=summary
        )
        
    except Exception as e:
        logger.error(f"Error analyzing questions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract-entities", response_model=EntityResponse)
async def extract_entities(request: ConversationRequest):
    """
    Extract named entities and relationships
    
    **Returns:**
    - Entities by type (people, tasks, technologies)
    - Relationships between entities
    - Most mentioned entities
    - Summary text
    """
    try:
        logger.info(f"Extracting entities from {len(request.messages)} messages")
        
        # Convert to dict format
        messages = [msg.dict() for msg in request.messages]
        
        # Extract entities from all messages
        all_entities = {
            'people': [],
            'tasks': [],
            'technologies': [],
            'urls': [],
            'emails': []
        }
        
        for msg in messages:
            entities = entity_recognizer.extract_entities(msg['text'])
            for entity_type in all_entities.keys():
                all_entities[entity_type].extend(entities.get(entity_type, []))
        
        # Extract relationships
        relationships = entity_recognizer.extract_relationships(messages)
        
        # Get most mentioned
        most_mentioned = {
            'tasks': entity_recognizer.get_most_mentioned_entities(messages, 'tasks', 10),
            'people': entity_recognizer.get_most_mentioned_entities(messages, 'people', 10),
            'technologies': entity_recognizer.get_most_mentioned_entities(messages, 'technologies', 10)
        }
        
        # Generate summary
        summary = entity_recognizer.summarize_entities(messages)
        
        return EntityResponse(
            entities=all_entities,
            relationships=relationships,
            most_mentioned=most_mentioned,
            summary=summary
        )
        
    except Exception as e:
        logger.error(f"Error extracting entities: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-full")
async def analyze_full_conversation(request: ConversationRequest):
    """
    Complete conversation analysis
    
    **Returns:**
    - Decisions
    - Questions
    - Entities
    - Combined insights
    """
    try:
        logger.info(f"Full analysis of {len(request.messages)} messages")
        
        # Run all analyses
        decisions_result = await analyze_decisions(request)
        questions_result = await analyze_questions(request)
        entities_result = await extract_entities(request)
        
        # Combine insights
        insights = []
        
        # Add decision insights
        if decisions_result.total_count > 0:
            insights.append({
                'type': 'decisions',
                'severity': 'info',
                'message': f"{decisions_result.total_count} decisions made",
                'details': decisions_result.by_type
            })
        
        # Add question insights
        if questions_result.unanswered_count > 0:
            severity = 'high' if questions_result.unanswered_count > 3 else 'medium'
            insights.append({
                'type': 'unanswered_questions',
                'severity': severity,
                'message': f"{questions_result.unanswered_count} unanswered questions",
                'details': questions_result.alerts
            })
        
        # Add entity insights
        task_count = len(entities_result.entities.get('tasks', []))
        if task_count > 0:
            insights.append({
                'type': 'tasks',
                'severity': 'info',
                'message': f"{task_count} tasks/issues mentioned",
                'details': entities_result.most_mentioned.get('tasks', [])[:5]
            })
        
        return {
            'decisions': decisions_result.dict(),
            'questions': questions_result.dict(),
            'entities': entities_result.dict(),
            'insights': insights,
            'message_count': len(request.messages)
        }
        
    except Exception as e:
        logger.error(f"Error in full analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))
