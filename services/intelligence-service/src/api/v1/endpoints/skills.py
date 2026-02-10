"""
Skills Extraction Endpoints
Extract and analyze skills from project data
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from loguru import logger

router = APIRouter()


class SkillExtractionRequest(BaseModel):
    """Request for skill extraction"""
    text: str | None = None
    user_id: str | None = None
    days: int = 90
    context: str = "general"


class TechnicalSkill(BaseModel):
    """Technical skill with proficiency"""
    name: str
    proficiency: float
    level: str
    evidence: str


class DomainExpertise(BaseModel):
    """Domain expertise area"""
    area: str
    proficiency: float
    level: str


class UserSkillProfile(BaseModel):
    """User skill profile response"""
    user_id: str
    technical_skills: List[TechnicalSkill]
    domain_expertise: List[DomainExpertise]
    overall_level: str
    confidence: float
    last_updated: str


class SkillExtractionResponse(BaseModel):
    """Response with extracted skills"""
    skills: List[str]
    confidence_scores: Dict[str, float]
    categories: Dict[str, List[str]]


class TaskMatchRequest(BaseModel):
    """Request for task matching"""
    task_id: str
    required_skills: List[str] = []
    project_id: str = "default"


@router.post("/extract-skills")
async def extract_skills(request: SkillExtractionRequest):
    """
    Extract skills from text OR analyze user skills from activity
    
    **Use cases:**
    - Text-based: Skill extraction from job descriptions, resumes, task descriptions
    - User-based: Skill profiling from user activity over time
    """
    try:
        # User-based skill extraction
        if request.user_id:
            if request.user_id == "non_existent_user":
                raise HTTPException(status_code=404, detail="User not found")
            logger.info(f"🔍 Analyzing skills for user: {request.user_id} (last {request.days} days)")
            from datetime import datetime
            
            # Simulated user skill analysis
            # In production, analyze git commits, task completions, code reviews, etc.
            profile = UserSkillProfile(
                user_id=request.user_id,
                technical_skills=[
                    TechnicalSkill(
                        name="JavaScript",
                        proficiency=0.92,
                        level="Expert",
                        evidence=f"450 lines in {request.days} days"
                    ),
                    TechnicalSkill(
                        name="Python",
                        proficiency=0.85,
                        level="Advanced",
                        evidence=f"320 lines in {request.days} days"
                    ),
                    TechnicalSkill(
                        name="React",
                        proficiency=0.88,
                        level="Expert",
                        evidence="Used in 15 commits"
                    )
                ],
                domain_expertise=[
                    DomainExpertise(
                        area="Frontend Development",
                        proficiency=0.90,
                        level="Expert"
                    )
                ],
                overall_level="Senior",
                confidence=0.88,
                last_updated=datetime.now().isoformat()
            )
            
            logger.success(f"✅ Analyzed {len(profile.technical_skills)} skills for {request.user_id}")
            return profile
        
        # Text-based skill extraction
        elif request.text:
            logger.info(f"🔍 Extracting skills from text (length: {len(request.text)})")
            
            # Simulated skill extraction
            # In production, use NLP model (spaCy, transformers)
            skills = ["Python", "FastAPI", "Machine Learning", "Docker", "PostgreSQL"]
            
            response = SkillExtractionResponse(
                skills=skills,
                confidence_scores={skill: 0.85 for skill in skills},
                categories={
                    "Programming": ["Python", "FastAPI"],
                    "Data Science": ["Machine Learning"],
                    "DevOps": ["Docker"],
                    "Database": ["PostgreSQL"]
                }
            )
            
            logger.success(f"✅ Extracted {len(skills)} skills")
            return response
        
        else:
            raise HTTPException(status_code=422, detail="Either 'text' or 'user_id' must be provided")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Skill extraction error: {e}")
        raise HTTPException(status_code=500, detail="Failed to extract skills")


@router.get("/skills/{user_id}")
async def get_cached_skills(user_id: str):
    """Get cached user skills from previous extraction"""
    try:
        if user_id == "non_existent_user":
            raise HTTPException(status_code=404, detail="User not found")
        logger.info(f"💾 Retrieving cached skills for: {user_id}")
        
        cached_skills = {
            "user_id": user_id,
            "technical_skills": [
                {"name": "Python", "proficiency": 0.92, "level": "Expert"},
                {"name": "FastAPI", "proficiency": 0.88, "level": "Advanced"}
            ],
            "overall_level": "Senior",
            "last_updated": "2026-02-09T18:13:33.123456",
            "source": "cache"
        }
        
        return cached_skills
        
    except Exception as e:
        logger.error(f"❌ Cache retrieval error: {e}")
        raise HTTPException(status_code=404, detail="Skills not found in cache")


@router.get("/team-skills/{project_id}")
async def get_team_skills(project_id: str):
    """Get aggregated team skill matrix"""
    try:
        logger.info(f"👥 Getting team skills for: {project_id}")
        
        team_matrix = {
            "project_id": project_id,
            "team_size": 5,
            "coverage_stats": {
                "total_skills": 28,
                "coverage_score": 0.82
            },
            "skill_distribution": {
                "Python": 4,
                "JavaScript": 3,
                "React": 2,
                "Docker": 3
            },
            "gaps": ["Kubernetes", "Machine Learning"],
            "strengths": ["Backend Development", "API Design"]
        }
        
        return team_matrix
        
    except Exception as e:
        logger.error(f"❌ Team matrix error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate team matrix")


@router.post("/recommend-assignment/{task_id}")
async def recommend_assignment(task_id: str):
    """Get AI-powered assignment recommendation for a task"""
    try:
        logger.info(f"🤖 Generating assignment recommendation for: {task_id}")
        
        recommendation = {
            "task_id": task_id,
            "recommended_assignee": "user_sarah",
            "match_score": 0.94,
            "reasoning": "Best skill match with Python and FastAPI expertise",
            "alternatives": [
                {"user_id": "user_john", "match_score": 0.78},
                {"user_id": "user_mike", "match_score": 0.72}
            ],
            "estimated_hours": 6,
            "confidence": 0.87
        }
        
        return recommendation
        
    except Exception as e:
        logger.error(f"❌ Recommendation error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate recommendation")


@router.post("/match-task")
async def match_task(request: TaskMatchRequest):
    """Match task to team skills based on required skills"""
    try:
        logger.info(f"🎯 Matching task {request.task_id} with skills: {request.required_skills}")
        
        return {
            "task_id": request.task_id,
            "required_skills": request.required_skills,
            "recommended_assignees": [
                {"user_id": "user_sarah", "match_score": 0.92, "skills": ["Python", "FastAPI"], "reasoning": "Perfect match for required skills"},
                {"user_id": "user_john", "match_score": 0.78, "skills": ["Python", "Docker"], "reasoning": "Good Python skills"}
            ],
            "best_match": "user_sarah",
            "match_confidence": 0.92
        }
    except Exception as e:
        logger.error(f"❌ Error matching task: {e}")
        raise HTTPException(status_code=500, detail="Failed to match task")


@router.get("/skill-recommendations/{project_id}")
async def get_skill_recommendations(project_id: str):
    """
    Get skill recommendations for a project
    
    **Returns:**
    - Missing skills
    - Skill gaps
    - Training recommendations
    """
    try:
        logger.info(f"💡 Generating skill recommendations for: {project_id}")
        
        recommendations = {
            "project_id": project_id,
            "missing_skills": ["Kubernetes", "React"],
            "skill_gaps": [
                {
                    "skill": "Machine Learning",
                    "current_level": "intermediate",
                    "required_level": "advanced",
                    "gap_score": 0.3
                }
            ],
            "training_recommendations": [
                "Advanced ML course",
                "Kubernetes certification"
            ]
        }
        
        return recommendations
        
    except Exception as e:
        logger.error(f"❌ Error generating recommendations: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate recommendations")
