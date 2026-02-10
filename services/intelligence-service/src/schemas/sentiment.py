"""
Pydantic schemas for sentiment analysis endpoints
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional


class SentimentAnalysisRequest(BaseModel):
    """Request for sentiment analysis"""
    user_id: str
    days: Optional[int] = Field(30, ge=7, le=90)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": "user_sarah",
                "days": 30
            }
        }
    )


class SentimentTrendResponse(BaseModel):
    """Sentiment trend analysis result"""
    user_id: str
    period_days: int
    sentiment_trend: Dict
    current_sentiment: Dict
    burnout_risk: Dict
    daily_scores: List[Dict]


class TeamMoraleResponse(BaseModel):
    """Team morale analysis result"""
    team_morale: Dict
    members_analyzed: int
    at_risk_members: List[Dict]
    high_morale_count: int
    low_morale_count: int
    member_details: Dict
