"""
Insights Endpoints
Generate actionable insights from project data
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from loguru import logger

router = APIRouter()


@router.get("/daily-insights/{project_id}")
async def get_daily_insights(project_id: str):
    """Generate comprehensive daily insights for a project"""
    try:
        logger.info(f"💡 Generating daily insights for: {project_id}")
        
        insights_data = {
            "project_id": project_id,
            "date": "2026-02-09",
            "summary": "Project Alpha made good progress today with 3 tasks completed and 3 PRs merged. Team morale remains healthy.",
            "highlights": [
                "✅ 3 tasks completed",
                "✅ 3 PRs merged",
                "✅ Zero critical blockers"
            ],
            "risks": [
                {
                    "type": "blocker",
                    "severity": "medium",
                    "description": "API integration pending external team",
                    "impact": "May delay sprint by 2-3 days"
                },
                {
                    "type": "resource",
                    "severity": "low",
                    "description": "Developer showing early burnout signs",
                    "impact": "Monitor workload and schedule 1:1"
                }
            ],
            "opportunities": [
                "Mike has availability for next 2 sprints - consider assigning high-priority features",
                "New automation tool could reduce testing time by 40%",
                "Client feedback positive - good time to propose scope expansion"
            ],
            "predictions": {
                "sprint_completion": "85% likely on time",
                "next_milestone": "92% confidence by March 15",
                "team_velocity": "Expected to increase 10% next sprint"
            },
            "metrics": {
                "velocity": 23.5,
                "team_morale": 0.72,
                "code_quality": 0.88,
                "timeline_confidence": 0.65
            },
            "generated_at": "2026-02-09T17:53:52.123456"
        }
        
        logger.success(f"✅ Generated insights with {len(insights_data['highlights'])} highlights")
        return insights_data
        
    except Exception as e:
        logger.error(f"❌ Error generating insights: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate daily insights")


@router.get("/project-health/{project_id}")
async def get_project_health(project_id: str):
    """Get overall project health score and metrics"""
    try:
        logger.info(f"💚 Checking health for: {project_id}")
        
        health_data = {
            "project_id": project_id,
            "overall_score": 78,
            "health_level": "Good",
            "components": {
                "timeline": {"score": 75, "status": "on_track"},
                "team_morale": {"score": 82, "status": "healthy"},
                "code_quality": {"score": 88, "status": "excellent"},
                "velocity": {"score": 70, "status": "moderate"}
            },
            "alerts": ["1 developer showing early burnout signs"],
            "recommendations": [
                "Schedule 1:1 with at-risk team member",
                "Consider adding sprint buffer"
            ],
            "last_updated": "2026-02-09T18:13:33.123456"
        }
        
        return health_data
        
    except Exception as e:
        logger.error(f"❌ Error checking project health: {e}")
        raise HTTPException(status_code=500, detail="Failed to get project health")


@router.get("/recommendations/{task_id}")
async def get_task_recommendations(task_id: str):
    """Get AI recommendations for a specific task"""
    try:
        logger.info(f"🎯 Getting recommendations for: {task_id}")
        
        recommendations = {
            "task_id": task_id,
            "assignment": {
                "recommended_assignee": "user_sarah",
                "match_score": 0.92,
                "reasoning": "Strong Python and FastAPI skills, 95% match"
            },
            "complexity": {
                "level": "medium",
                "estimated_hours": 8,
                "confidence": 0.85
            },
            "dependencies": ["task_042", "task_067"],
            "risks": [
                "Requires API keys from external team",
                "May need additional backend support"
            ],
            "suggestions": [
                "Pair with senior dev for first day",
                "Schedule mid-task check-in",
                "Allocate 20% buffer for unknowns"
            ]
        }
        
        return recommendations
        
    except Exception as e:
        logger.error(f"❌ Error generating recommendations: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate recommendations")


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
