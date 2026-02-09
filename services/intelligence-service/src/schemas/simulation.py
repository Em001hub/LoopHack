"""
Pydantic schemas for simulation endpoints
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class SimulationRequest(BaseModel):
    """Request for Monte Carlo simulation"""
    project_id: str
    n_simulations: Optional[int] = Field(1000, ge=100, le=10000)
    scenario_params: Optional[Dict] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "project_id": "proj_alpha",
                "n_simulations": 1000,
                "scenario_params": {
                    "add_developers": 2,
                    "remove_features": 20
                }
            }
        }


class SimulationResponse(BaseModel):
    """Simulation results"""
    simulation_count: int
    predicted_weeks: Dict
    percentiles: Dict
    completion_dates: Dict
    risk_analysis: Dict
    distribution: Dict
    scenario_params: Dict
    probability_on_time: Optional[float] = None


class ScenarioComparisonRequest(BaseModel):
    """Request for scenario comparison"""
    project_id: str
    scenarios: List[Dict]
    n_simulations: Optional[int] = Field(1000, ge=100, le=5000)
    
    class Config:
        json_schema_extra = {
            "example": {
                "project_id": "proj_alpha",
                "scenarios": [
                    {
                        "name": "Add 2 devs",
                        "add_developers": 2
                    },
                    {
                        "name": "Cut features",
                        "remove_features": 30
                    }
                ],
                "n_simulations": 1000
            }
        }


class ScenarioComparisonResponse(BaseModel):
    """Scenario comparison results"""
    scenarios: Dict
    comparison_table: List[Dict]
    recommendation: str
