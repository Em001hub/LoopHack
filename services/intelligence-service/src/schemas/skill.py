"""
Pydantic schemas for skill extraction endpoints
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class SkillExtractionRequest(BaseModel):
    """Request for skill extraction"""
    user_id: str = Field(..., description="User ID to analyze")
    days: Optional[int] = Field(90, description="Days of history to analyze")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_sarah",
                "days": 90
            }
        }


class TechnicalSkill(BaseModel):
    """Individual technical skill"""
    name: str
    proficiency: float = Field(..., ge=0, le=1)
    level: str
    evidence: str


class DomainExpertise(BaseModel):
    """Domain expertise area"""
    area: str
    proficiency: float
    level: str


class SkillProfileResponse(BaseModel):
    """User skill profile"""
    user_id: str
    technical_skills: List[TechnicalSkill]
    domain_expertise: List[DomainExpertise]
    overall_level: str
    confidence: float
    last_updated: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_sarah",
                "technical_skills": [
                    {
                        "name": "JavaScript",
                        "proficiency": 0.92,
                        "level": "Expert",
                        "evidence": "450 lines in 90 days"
                    }
                ],
                "domain_expertise": [
                    {
                        "area": "Frontend Development",
                        "proficiency": 0.90,
                        "level": "Expert"
                    }
                ],
                "overall_level": "Senior",
                "confidence": 0.88,
                "last_updated": "2024-02-09T10:00:00Z"
            }
        }


class TaskMatchRequest(BaseModel):
    """Request for task-skill matching"""
    user_id: str
    task_id: str
    task_requirements: Dict = Field(..., description="Required and preferred skills")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_sarah",
                "task_id": "PROJ-123",
                "task_requirements": {
                    "required_skills": ["React", "JavaScript"],
                    "preferred_skills": ["TypeScript", "Redux"]
                }
            }
        }


class TaskMatchResponse(BaseModel):
    """Task matching result"""
    match_score: float
    required_skills_matched: List[str]
    required_skills_missing: List[str]
    preferred_skills_matched: List[str]
    recommendation: str
    confidence: float
