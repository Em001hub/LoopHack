"""
Pydantic schemas for prediction endpoints
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime


class TimelinePredictionRequest(BaseModel):
    """Request model for timeline prediction"""
    project_id: str = Field(..., description="Unique project identifier")
    target_date: Optional[datetime] = Field(None, description="Target completion date")
    
    class Config:
        json_schema_extra = {
            "example": {
                "project_id": "proj_123",
                "target_date": "2024-12-31T00:00:00Z"
            }
        }


class ConfidenceIntervals(BaseModel):
    """Confidence intervals for predictions"""
    p10: str = Field(..., description="10th percentile (optimistic)")
    p50: str = Field(..., description="50th percentile (median)")
    p90: str = Field(..., description="90th percentile (pessimistic)")


class TimelinePredictionResponse(BaseModel):
    """Response model for timeline prediction"""
    project_id: str
    predicted_completion_date: str
    predicted_weeks_remaining: float
    confidence_intervals: ConfidenceIntervals
    probability_on_time: Optional[float] = Field(None, description="Probability of meeting target (0-1)")
    risk_factors: List[str] = Field(default_factory=list)
    model_confidence: float = Field(..., description="Model confidence score (0-1)")
    note: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "project_id": "proj_123",
                "predicted_completion_date": "2024-11-15T00:00:00Z",
                "predicted_weeks_remaining": 8.5,
                "confidence_intervals": {
                    "p10": "2024-10-30T00:00:00Z",
                    "p50": "2024-11-15T00:00:00Z",
                    "p90": "2024-12-01T00:00:00Z"
                },
                "probability_on_time": 0.75,
                "risk_factors": ["3 blocked tasks", "High velocity variance"],
                "model_confidence": 0.85,
                "created_at": "2024-09-20T10:30:00Z"
            }
        }


class PredictionHistory(BaseModel):
    """Historical prediction record"""
    id: str
    project_id: str
    predicted_date: str
    actual_date: Optional[str] = None
    accuracy: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
