"""
Simulation Endpoints
Run what-if scenarios and project simulations
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from loguru import logger

router = APIRouter()


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
