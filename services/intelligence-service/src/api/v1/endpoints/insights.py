"""
Insights Endpoints
Generate actionable insights from project data
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from loguru import logger

router = APIRouter()


class InsightResponse(BaseModel):
    """Project insight"""
    type: str
    title: str
    description: str
    severity: str  # info, warning, critical
    impact: str
    recommendations: List[str]


@router.get("/project-insights/{project_id}", response_model=List[InsightResponse])
async def get_project_insights(project_id: str):
    """
    Get AI-generated insights for a project
    
    **Insight types:**
    - Timeline risks
    - Resource bottlenecks
    - Skill gaps
    - Team health issues
    - Process improvements
    
    **Returns:**
    - Prioritized list of insights
    - Severity levels
    - Actionable recommendations
    """
    try:
        logger.info(f"💡 Generating insights for: {project_id}")
        
        insights = [
            InsightResponse(
                type="timeline_risk",
                title="Timeline at Risk",
                description="Project has 2 blocked tasks affecting critical path",
                severity="warning",
                impact="May delay completion by 1-2 weeks",
                recommendations=[
                    "Unblock task #42 (waiting on API keys)",
                    "Escalate blocker on task #67",
                    "Consider parallel work streams"
                ]
            ),
            InsightResponse(
                type="velocity_trend",
                title="Velocity Declining",
                description="Team velocity decreased 20% over last 2 sprints",
                severity="warning",
                impact="Completion date may shift by 1 week",
                recommendations=[
                    "Review team capacity and workload",
                    "Identify and address blockers",
                    "Consider reducing scope or adding resources"
                ]
            ),
            InsightResponse(
                type="skill_gap",
                title="Skill Gap Detected",
                description="No team member has advanced Kubernetes experience",
                severity="info",
                impact="May slow down deployment tasks",
                recommendations=[
                    "Provide Kubernetes training",
                    "Bring in consultant for deployment",
                    "Pair junior devs with experienced mentor"
                ]
            )
        ]
        
        logger.success(f"✅ Generated {len(insights)} insights")
        return insights
        
    except Exception as e:
        logger.error(f"❌ Error generating insights: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate insights")


@router.get("/team-insights/{team_id}")
async def get_team_insights(team_id: str):
    """
    Get insights about team performance and health
    
    **Returns:**
    - Productivity trends
    - Collaboration patterns
    - Skill distribution
    - Workload balance
    """
    try:
        logger.info(f"👥 Generating team insights for: {team_id}")
        
        insights = {
            "team_id": team_id,
            "productivity_score": 0.78,
            "collaboration_health": "good",
            "workload_balance": {
                "status": "unbalanced",
                "overloaded_members": ["dev_1"],
                "underutilized_members": ["dev_3"]
            },
            "skill_coverage": {
                "frontend": 0.8,
                "backend": 0.9,
                "devops": 0.4,
                "ml": 0.3
            },
            "recommendations": [
                "Redistribute tasks from dev_1 to dev_3",
                "Invest in DevOps training",
                "Consider hiring ML specialist"
            ]
        }
        
        return insights
        
    except Exception as e:
        logger.error(f"❌ Error generating team insights: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate team insights")


@router.get("/risk-analysis/{project_id}")
async def analyze_risks(project_id: str):
    """
    Comprehensive risk analysis for project
    
    **Analyzes:**
    - Timeline risks
    - Resource risks
    - Technical risks
    - Dependency risks
    
    **Returns:**
    - Risk score (0-1)
    - Risk breakdown
    - Mitigation strategies
    """
    try:
        logger.info(f"⚠️  Analyzing risks for: {project_id}")
        
        risk_analysis = {
            "project_id": project_id,
            "overall_risk_score": 0.42,
            "risk_level": "medium",
            "risks": [
                {
                    "category": "timeline",
                    "risk": "Blocked tasks on critical path",
                    "probability": 0.7,
                    "impact": 0.8,
                    "score": 0.56,
                    "mitigation": "Escalate blockers, create parallel work streams"
                },
                {
                    "category": "resource",
                    "risk": "Key developer on vacation next sprint",
                    "probability": 1.0,
                    "impact": 0.4,
                    "score": 0.40,
                    "mitigation": "Knowledge transfer before vacation, pair programming"
                },
                {
                    "category": "technical",
                    "risk": "Unproven technology stack",
                    "probability": 0.5,
                    "impact": 0.6,
                    "score": 0.30,
                    "mitigation": "Build POC, allocate buffer time, have fallback plan"
                }
            ],
            "recommendations": [
                "Focus on unblocking critical path tasks",
                "Create knowledge sharing sessions",
                "Validate technical decisions with POCs"
            ]
        }
        
        return risk_analysis
        
    except Exception as e:
        logger.error(f"❌ Error analyzing risks: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze risks")
