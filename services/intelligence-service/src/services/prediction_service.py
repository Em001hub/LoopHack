"""
Prediction Service
Business logic for timeline predictions and project intelligence
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from loguru import logger

from src.ml.models.timeline_predictor import TimelinePredictor
from src.schemas.prediction import (
    TimelinePredictionResponse,
    ConfidenceIntervals,
    PredictionHistory
)


class PredictionService:
    """Service for handling prediction logic"""
    
    def __init__(self):
        self.predictor = TimelinePredictor()
    
    async def predict_project_timeline(
        self,
        db: AsyncSession,
        project_id: str,
        target_date: Optional[datetime] = None
    ) -> TimelinePredictionResponse:
        """
        Generate timeline prediction for a project
        
        **Process:**
        1. Fetch project data from database
        2. Extract features
        3. Run ML prediction
        4. Store prediction history
        5. Return formatted response
        """
        try:
            logger.info(f"📊 Generating prediction for project: {project_id}")
            
            # Fetch project data (simulated for now)
            project_data = await self._fetch_project_data(db, project_id)
            
            # Add target date to project data
            if target_date:
                project_data['target_date'] = target_date
            
            # Run prediction
            prediction_result = self.predictor.predict_completion_date(
                project_data=project_data,
                run_monte_carlo=True
            )
            
            # Format response
            response = TimelinePredictionResponse(
                project_id=project_id,
                predicted_completion_date=prediction_result['predicted_completion_date'],
                predicted_weeks_remaining=prediction_result['predicted_weeks_remaining'],
                confidence_intervals=ConfidenceIntervals(**prediction_result['confidence_intervals']),
                probability_on_time=prediction_result.get('probability_on_time'),
                risk_factors=prediction_result['risk_factors'],
                model_confidence=prediction_result['model_confidence'],
                note=prediction_result.get('note')
            )
            
            # Store prediction in history (would be database in production)
            logger.info(f"✅ Prediction generated successfully")
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Prediction service error: {e}")
            raise
    
    async def _fetch_project_data(
        self,
        db: AsyncSession,
        project_id: str
    ) -> Dict:
        """
        Fetch project data from database
        
        **In production, this would:**
        - Query tasks, sprints, team members
        - Calculate velocity metrics
        - Aggregate complexity scores
        - Identify blockers
        
        **For now, returns simulated data**
        """
        logger.info(f"Fetching project data for: {project_id}")
        
        # Simulated project data
        # In production, this would query the database
        simulated_data = {
            'remaining_story_points': 120,
            'avg_weekly_velocity': 15,
            'velocity_std': 3,
            'team_size': 5,
            'blocked_tasks_count': 2,
            'high_complexity_count': 8,
            'avg_task_age_days': 7,
            'team_experience_score': 0.75
        }
        
        logger.info(f"✅ Project data fetched: {simulated_data}")
        return simulated_data
    
    async def get_prediction_history(
        self,
        db: AsyncSession,
        project_id: str,
        limit: int = 10
    ) -> List[PredictionHistory]:
        """
        Get historical predictions for a project
        
        **In production:**
        - Query prediction_history table
        - Calculate accuracy metrics
        - Return sorted by date
        """
        logger.info(f"Fetching prediction history for: {project_id}")
        
        # Simulated history
        # In production, query database
        history = [
            PredictionHistory(
                id=f"pred_{i}",
                project_id=project_id,
                predicted_date=(datetime.now() + timedelta(weeks=8-i)).isoformat(),
                actual_date=None,
                accuracy=None,
                created_at=datetime.now() - timedelta(days=i*7)
            )
            for i in range(min(limit, 5))
        ]
        
        logger.info(f"✅ Retrieved {len(history)} historical predictions")
        return history
    
    async def calculate_team_velocity(
        self,
        db: AsyncSession,
        project_id: str,
        weeks: int = 4
    ) -> Dict:
        """
        Calculate team velocity metrics
        
        **Returns:**
        - avg_velocity: Mean story points per week
        - std_velocity: Standard deviation
        - trend: Increasing/Decreasing/Stable
        """
        logger.info(f"Calculating velocity for project: {project_id}")
        
        # Simulated velocity calculation
        # In production, aggregate sprint data
        velocity_data = {
            'avg_velocity': 15.0,
            'std_velocity': 3.0,
            'trend': 'stable',
            'weeks_analyzed': weeks
        }
        
        return velocity_data
    
    async def identify_blockers(
        self,
        db: AsyncSession,
        project_id: str
    ) -> List[Dict]:
        """
        Identify current blockers affecting timeline
        
        **Returns list of:**
        - blocker_id
        - task_id
        - blocker_type
        - days_blocked
        - impact_score
        """
        logger.info(f"Identifying blockers for: {project_id}")
        
        # Simulated blocker data
        blockers = [
            {
                'blocker_id': 'block_1',
                'task_id': 'task_42',
                'blocker_type': 'dependency',
                'days_blocked': 5,
                'impact_score': 0.8
            },
            {
                'blocker_id': 'block_2',
                'task_id': 'task_67',
                'blocker_type': 'resource',
                'days_blocked': 3,
                'impact_score': 0.6
            }
        ]
        
        return blockers
