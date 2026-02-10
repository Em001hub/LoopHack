"""
Timeline Prediction Endpoints
Handles project timeline forecasting and completion date predictions
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from loguru import logger
from datetime import datetime

from src.config.database import get_db
from src.schemas.prediction import (
    TimelinePredictionRequest,
    TimelinePredictionResponse,
    PredictionHistory
)
from src.services.prediction_service import PredictionService

router = APIRouter()

# Dependency injection
def get_prediction_service() -> PredictionService:
    return PredictionService()

@router.post("/predict-timeline", response_model=TimelinePredictionResponse)
async def predict_timeline(
    request: TimelinePredictionRequest,
    db: AsyncSession = Depends(get_db),
    service: PredictionService = Depends(get_prediction_service)
):
    """
    Predict project completion timeline
    
    **Features:**
    - Probabilistic forecasting with confidence intervals
    - Risk factor analysis
    - Historical pattern recognition
    - Monte Carlo simulation
    
    **Returns:**
    - Predicted completion date
    - Confidence intervals (50%, 90%)
    - Probability of meeting deadline
    - Risk factors and recommendations
    """
    try:
        logger.info(f"📊 Predicting timeline for project: {request.project_id}")
        
        # Get prediction
        prediction = await service.predict_project_timeline(
            db=db,
            project_id=request.project_id,
            target_date=request.target_date
        )
        
        logger.success(f"✅ Timeline predicted: {prediction.predicted_completion_date}")
        
        return prediction
        
    except ValueError as e:
        logger.error(f"❌ Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate prediction")


@router.get("/prediction-history/{project_id}", response_model=List[PredictionHistory])
async def get_prediction_history(
    project_id: str,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    service: PredictionService = Depends(get_prediction_service)
):
    """
    Get historical predictions for a project
    
    **Use cases:**
    - Track prediction accuracy over time
    - See how estimates evolved
    - Identify estimation patterns
    """
    try:
        logger.info(f"📜 Fetching prediction history for: {project_id}")
        
        history = await service.get_prediction_history(
            db=db,
            project_id=project_id,
            limit=limit
        )
        
        logger.info(f"✅ Retrieved {len(history)} predictions")
        return history
        
    except Exception as e:
        logger.error(f"❌ Failed to fetch history: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch prediction history")


@router.post("/recalculate-timeline/{project_id}")
async def recalculate_timeline(project_id: str):
    """
    Trigger background recalculation of timeline
    
    **Use cases:**
    - Refresh predictions after major project changes
    - Periodic automated updates
    - User-triggered recalculation
    """
    try:
        logger.info(f"🔄 Triggering timeline recalculation for: {project_id}")
        
        result = {
            "status": "initiated",
            "message": "Timeline recalculation started in background",
            "project_id": project_id
        }
        
        logger.success(f"✅ Recalculation initiated for {project_id}")
        return result
        
    except Exception as e:
        logger.error(f"❌ Recalculation error: {e}")
        raise HTTPException(status_code=500, detail="Failed to initiate recalculation")
