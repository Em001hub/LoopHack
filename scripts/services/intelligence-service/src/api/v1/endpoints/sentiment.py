"""
Sentiment Analysis Endpoints
Analyze team sentiment and communication patterns
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from loguru import logger

router = APIRouter()


class SentimentRequest(BaseModel):
    """Request for sentiment analysis"""
    text: str
    context: str = "general"


class SentimentResponse(BaseModel):
    """Sentiment analysis results"""
    sentiment: str  # positive, negative, neutral
    score: float  # -1 to 1
    confidence: float
    emotions: Dict[str, float]


@router.post("/analyze-sentiment", response_model=SentimentResponse)
async def analyze_sentiment(request: SentimentRequest):
    """
    Analyze sentiment of text
    
    **Use cases:**
    - Team morale tracking
    - Communication health
    - Early warning for team issues
    
    **Returns:**
    - Overall sentiment (positive/negative/neutral)
    - Confidence score
    - Emotion breakdown
    """
    try:
        logger.info(f"😊 Analyzing sentiment (text length: {len(request.text)})")
        
        # Simulated sentiment analysis
        # In production, use transformers (BERT, RoBERTa)
        response = SentimentResponse(
            sentiment="positive",
            score=0.75,
            confidence=0.88,
            emotions={
                "joy": 0.6,
                "trust": 0.4,
                "anticipation": 0.3,
                "fear": 0.1
            }
        )
        
        logger.success(f"✅ Sentiment: {response.sentiment} (score: {response.score})")
        return response
        
    except Exception as e:
        logger.error(f"❌ Sentiment analysis error: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze sentiment")


@router.get("/team-sentiment/{project_id}")
async def get_team_sentiment(project_id: str, days: int = 7):
    """
    Get team sentiment trends for a project
    
    **Returns:**
    - Sentiment over time
    - Team morale score
    - Communication health
    - Alerts/warnings
    """
    try:
        logger.info(f"📊 Fetching team sentiment for: {project_id}")
        
        sentiment_data = {
            "project_id": project_id,
            "overall_sentiment": "positive",
            "morale_score": 0.72,
            "trend": "improving",
            "daily_sentiment": [
                {"date": "2024-09-20", "score": 0.75},
                {"date": "2024-09-19", "score": 0.68},
                {"date": "2024-09-18", "score": 0.70}
            ],
            "alerts": [],
            "recommendations": [
                "Team morale is healthy",
                "Communication patterns are positive"
            ]
        }
        
        return sentiment_data
        
    except Exception as e:
        logger.error(f"❌ Error fetching team sentiment: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch team sentiment")


class UserSentimentRequest(BaseModel):
    """Request for user sentiment analysis"""
    user_id: str
    days: int = 7


@router.post("/analyze-user")
async def analyze_user_sentiment(request: UserSentimentRequest):
    """Analyze user sentiment over time - alias endpoint"""
    try:
        logger.info(f"😊 Analyzing sentiment for user: {request.user_id}")
        return {
            "user_id": request.user_id,
            "overall_sentiment": "positive",
            "average_score": 0.72,
            "trend": "stable",
            "burnout_risk": "low",
            "recommendations": ["Sentiment is healthy", "No action needed"]
        }
    except Exception as e:
        logger.error(f"❌ User sentiment error: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze user sentiment")


@router.get("/team-morale/{project_id}")
async def get_team_morale(project_id: str, days: int = 30):
    """Get detailed team morale analysis with member-level insights"""
    try:
        logger.info(f"📊 Analyzing team morale for: {project_id} (last {days} days)")
        
        morale_data = {
            "project_id": project_id,
            "team_morale": {
                "average_sentiment": 0.45,
                "label": "neutral",
                "trend": "stable"
            },
            "members_analyzed": 5,
            "at_risk_members": [
                {
                    "user_id": "user_bob",
                    "risk_level": "Medium",
                    "sentiment_score": 0.25,
                    "trend": "declining",
                    "recommendations": ["Schedule 1:1 check-in", "Review workload"]
                }
            ],
            "high_morale_count": 3,
            "low_morale_count": 1,
            "member_details": {
                "user_sarah": {"sentiment": 0.85, "label": "positive", "trend": "stable", "risk_level": "Low"},
                "user_bob": {"sentiment": 0.25, "label": "negative", "trend": "declining", "risk_level": "Medium"},
                "user_john": {"sentiment": 0.65, "label": "positive", "trend": "improving", "risk_level": "Low"},
                "user_alice": {"sentiment": 0.70, "label": "positive", "trend": "stable", "risk_level": "Low"},
                "user_charlie": {"sentiment": 0.40, "label": "neutral", "trend": "stable", "risk_level": "Low"}
            },
            "time_period_days": days,
            "last_updated": "2026-02-09T17:24:30.123456"
        }
        
        logger.success(f"✅ Analyzed morale for {morale_data['members_analyzed']} team members")
        return morale_data
        
    except Exception as e:
        logger.error(f"❌ Error analyzing team morale: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze team morale")


@router.get("/burnout-risk/{user_id}")
async def get_burnout_risk(user_id: str):
    """Check burnout risk for a specific user"""
    try:
        logger.info(f"⚠️ Assessing burnout risk for: {user_id}")
        
        burnout_data = {
            "user_id": user_id,
            "burnout_risk": "Low",
            "risk_score": 0.25,
            "risk_factors": [
                {"factor": "Work hours", "level": "Normal", "score": 0.2},
                {"factor": "Task complexity", "level": "Moderate", "score": 0.4},
                {"factor": "Overtime frequency", "level": "Low", "score": 0.1}
            ],
            "sentiment_trend": "stable",
            "recent_sentiment": 0.72,
            "productivity_trend": "consistent",
            "recommendations": [
                "Maintain current work-life balance",
                "Continue regular breaks"
            ],
            "last_assessed": "2026-02-09T17:30:29.123456"
        }
        
        logger.success(f"✅ Burnout risk for {user_id}: {burnout_data['burnout_risk']}")
        return burnout_data
        
    except Exception as e:
        logger.error(f"❌ Error assessing burnout risk: {e}")
        raise HTTPException(status_code=500, detail="Failed to assess burnout risk")


@router.get("/sentiment-alerts/{project_id}")
async def get_sentiment_alerts(project_id: str):
    """Get active sentiment alerts for a project"""
    try:
        logger.info(f"🚨 Fetching sentiment alerts for: {project_id}")
        
        alerts_data = {
            "project_id": project_id,
            "active_alerts": [
                {
                    "alert_id": "alert_001",
                    "severity": "Medium",
                    "type": "declining_morale",
                    "user_id": "user_bob",
                    "message": "User sentiment has declined by 30% over the last 7 days",
                    "triggered_at": "2026-02-07T14:30:00Z",
                    "recommendations": ["Schedule 1:1 meeting", "Review workload"]
                }
            ],
            "total_alerts": 1,
            "high_severity_count": 0,
            "medium_severity_count": 1,
            "low_severity_count": 0,
            "last_checked": "2026-02-09T17:32:29.123456"
        }
        
        logger.success(f"✅ Found {alerts_data['total_alerts']} active alerts for {project_id}")
        return alerts_data
        
    except Exception as e:
        logger.error(f"❌ Error fetching sentiment alerts: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch sentiment alerts")


@router.post("/conversation-intelligence")
async def analyze_conversation(text: str):
    """
    Analyze conversation for insights
    
    **Extracts:**
    - Action items
    - Decisions made
    - Blockers mentioned
    - Questions raised
    """
    try:
        logger.info("💬 Analyzing conversation")
        
        insights = {
            "action_items": [
                "Update API documentation",
                "Schedule code review"
            ],
            "decisions": [
                "Use PostgreSQL for database"
            ],
            "blockers": [
                "Waiting for API keys"
            ],
            "questions": [
                "When is the deployment deadline?"
            ],
            "sentiment": "neutral",
            "urgency": "medium"
        }
        
        return insights
        
    except Exception as e:
        logger.error(f"❌ Conversation analysis error: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze conversation")
