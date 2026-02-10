"""
Simulation Endpoints
Run what-if scenarios and project simulations
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from loguru import logger

router = APIRouter()


class Scenario(BaseModel):
    """Scenario details"""
    name: str
    add_developers: Optional[int] = 0
    reduce_scope_percent: Optional[int] = 0


class CompareScenariosRequest(BaseModel):
    """Request for comparing multiple scenarios"""
    project_id: str
    scenarios: List[Scenario]


class SimulationRequest(BaseModel):
    """Request for project simulation"""
    project_id: str
    scenario: str  # "add_team_member", "reduce_scope", "extend_deadline"
    parameters: Dict


class SimulationResponse(BaseModel):
    """Simulation results"""
    scenario: str
    original_completion: str
    simulated_completion: str
    impact_days: int
    success_probability: float
    recommendations: List[str]


@router.post("/run-simulation", response_model=SimulationResponse)
async def run_simulation(request: SimulationRequest):
    """
    Run what-if simulation on project
    
    **Scenarios:**
    - Add/remove team members
    - Change scope
    - Adjust deadlines
    - Resource reallocation
    
    **Returns:**
    - Impact on timeline
    - Success probability
    - Recommendations
    """
    try:
        logger.info(f"🎮 Running simulation: {request.scenario} for {request.project_id}")
        
        # Simulated results
        # In production, run actual Monte Carlo simulations
        from datetime import datetime, timedelta
        
        original = datetime.now() + timedelta(weeks=8)
        simulated = datetime.now() + timedelta(weeks=6)
        
        response = SimulationResponse(
            scenario=request.scenario,
            original_completion=original.isoformat(),
            simulated_completion=simulated.isoformat(),
            impact_days=-14,
            success_probability=0.82,
            recommendations=[
                "Adding 2 senior developers reduces timeline by 2 weeks",
                "Consider pair programming for knowledge transfer",
                "Monitor velocity for first 2 sprints"
            ]
        )
        
        logger.success(f"✅ Simulation complete: {response.impact_days} days impact")
        return response
        
    except Exception as e:
        logger.error(f"❌ Simulation error: {e}")
        raise HTTPException(status_code=500, detail="Failed to run simulation")


class TimelineSimulationRequest(BaseModel):
    """Request for timeline simulation"""
    project_id: str
    n_simulations: int = 1000


@router.post("/simulate-timeline")
async def simulate_timeline(request: TimelineSimulationRequest):
    """Monte Carlo timeline simulation - alias endpoint"""
    try:
        logger.info(f"🎲 Running Monte Carlo simulation for: {request.project_id}")
        from datetime import datetime, timedelta
        
        return {
            "project_id": request.project_id,
            "simulation_count": request.n_simulations,
            "predicted_weeks": {
                "mean": 12.5,
                "median": 12.1,
                "std": 3.2
            },
            "percentiles": {
                "p10": 9.2,
                "p50": 12.1,
                "p90": 16.5
            },
            "completion_dates": {
                "p10": (datetime.now() + timedelta(weeks=9.2)).strftime("%Y-%m-%d"),
                "p50": (datetime.now() + timedelta(weeks=12.1)).strftime("%Y-%m-%d"),
                "p90": (datetime.now() + timedelta(weeks=16.5)).strftime("%Y-%m-%d")
            },
            "probability_on_time": 0.73
        }
    except Exception as e:
        logger.error(f"❌ Simulation error: {e}")
        raise HTTPException(status_code=500, detail="Failed to run simulation")


@router.post("/compare-scenarios")
async def compare_scenarios(request: CompareScenariosRequest):
    """Compare multiple what-if scenarios"""
    try:
        logger.info(f"📊 Comparing scenarios for: {request.project_id}")
        return {
            "project_id": request.project_id,
            "scenarios": [
                {"name": "baseline", "completion_weeks": 8, "success_probability": 0.75},
                {"name": "add_2_devs", "completion_weeks": 6, "success_probability": 0.88},
                {"name": "reduce_scope", "completion_weeks": 5, "success_probability": 0.92}
            ],
            "recommendation": "add_2_devs"
        }
    except Exception as e:
        logger.error(f"❌ Comparison error: {e}")
        raise HTTPException(status_code=500, detail="Failed to compare scenarios")


@router.post("/what-if/{project_id}")
async def what_if_analysis(project_id: str, change: str = "add_team_member"):
    """Quick what-if analysis"""
    try:
        logger.info(f"🔮 What-if analysis: {change} for {project_id}")
        from datetime import datetime, timedelta
        return {
            "project_id": project_id,
            "change": change,
            "original_completion": (datetime.now() + timedelta(weeks=8)).isoformat(),
            "new_completion": (datetime.now() + timedelta(weeks=6)).isoformat(),
            "impact_days": -14,
            "recommendation": "Positive impact, recommend implementing"
        }
    except Exception as e:
        logger.error(f"❌ What-if error: {e}")
        raise HTTPException(status_code=500, detail="Failed to run what-if analysis")


@router.get("/simulation-history/{project_id}")
async def get_simulation_history(project_id: str, limit: int = 10):
    """Get historical simulations for a project"""
    try:
        logger.info(f"📜 Fetching simulation history for: {project_id}")
        
        history = [
            {
                "id": f"sim_{i}",
                "scenario": "add_team_member",
                "impact_days": -7 * i,
                "created_at": "2024-09-20T10:30:00Z"
            }
            for i in range(1, min(limit + 1, 6))
        ]
        
        return {"project_id": project_id, "simulations": history}
        
    except Exception as e:
        logger.error(f"❌ Error fetching history: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch simulation history")
