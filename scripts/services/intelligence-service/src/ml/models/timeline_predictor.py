"""
Timeline Prediction Model
Predicts project completion dates using historical data and ML
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from loguru import logger
import pickle
import os


class TimelinePredictor:
    """
    Machine Learning model for predicting project timelines
    
    **Approach:**
    1. Extract features from project data
    2. Train Random Forest on historical projects
    3. Generate probabilistic predictions
    4. Run Monte Carlo simulations for confidence intervals
    """
    
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_names = [
            'remaining_story_points',
            'avg_weekly_velocity',
            'velocity_std',
            'team_size',
            'blocked_tasks_count',
            'high_complexity_count',
            'avg_task_age_days',
            'team_experience_score'
        ]
    
    def extract_features(self, project_data: Dict) -> np.ndarray:
        """
        Extract ML features from project data
        
        **Features:**
        - Work remaining (story points)
        - Team velocity (mean & variance)
        - Team composition & experience
        - Current blockers
        - Task complexity distribution
        - Historical patterns
        """
        try:
            features = [
                project_data.get('remaining_story_points', 0),
                project_data.get('avg_weekly_velocity', 1),
                project_data.get('velocity_std', 0),
                project_data.get('team_size', 1),
                project_data.get('blocked_tasks_count', 0),
                project_data.get('high_complexity_count', 0),
                project_data.get('avg_task_age_days', 0),
                project_data.get('team_experience_score', 0.5)
            ]
            
            return np.array(features).reshape(1, -1)
            
        except Exception as e:
            logger.error(f"Feature extraction error: {e}")
            raise ValueError(f"Invalid project data: {e}")
    
    def predict_completion_date(
        self,
        project_data: Dict,
        run_monte_carlo: bool = True
    ) -> Dict:
        """
        Predict project completion with confidence intervals
        
        **Returns:**
        - predicted_completion_date: Most likely completion
        - confidence_50: 50% confidence interval
        - confidence_90: 90% confidence interval
        - probability_on_time: Likelihood of meeting target
        - risk_factors: List of identified risks
        """
        try:
            logger.info("🔮 Generating timeline prediction...")
            
            if not self.is_trained:
                logger.warning("⚠️  Model not trained, using heuristic approach")
                return self._heuristic_prediction(project_data)
            
            # Extract features
            features = self.extract_features(project_data)
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            # Predict weeks remaining
            predicted_weeks = self.model.predict(features_scaled)[0]
            
            # Calculate completion date
            predicted_date = datetime.now() + timedelta(weeks=predicted_weeks)
            
            # Run Monte Carlo simulation for confidence intervals
            if run_monte_carlo:
                mc_results = self._monte_carlo_simulation(project_data, n_simulations=1000)
            else:
                mc_results = self._simple_confidence(predicted_weeks)
            
            # Identify risk factors
            risk_factors = self._identify_risk_factors(project_data)
            
            # Calculate probability of meeting target
            target_date = project_data.get('target_date')
            probability_on_time = self._calculate_probability(
                mc_results['simulations'],
                target_date
            ) if target_date else None
            
            result = {
                'predicted_completion_date': predicted_date.isoformat(),
                'predicted_weeks_remaining': float(predicted_weeks),
                'confidence_intervals': {
                    'p10': mc_results['p10'].isoformat(),
                    'p50': mc_results['p50'].isoformat(),
                    'p90': mc_results['p90'].isoformat()
                },
                'probability_on_time': probability_on_time,
                'risk_factors': risk_factors,
                'model_confidence': 0.85 if self.is_trained else 0.60
            }
            
            logger.success(f"✅ Prediction complete: {predicted_date.date()}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Prediction failed: {e}")
            raise
    
    def _heuristic_prediction(self, project_data: Dict) -> Dict:
        """
        Fallback heuristic when ML model not available
        
        **Simple formula:**
        weeks = (remaining_points / velocity) * risk_multiplier
        """
        logger.info("Using heuristic prediction (no trained model)")
        
        remaining_points = project_data.get('remaining_story_points', 0)
        velocity = max(project_data.get('avg_weekly_velocity', 1), 1)
        
        # Base estimate
        base_weeks = remaining_points / velocity
        
        # Apply risk multipliers
        risk_multiplier = 1.0
        
        # Blockers add 10% delay each
        blocked_count = project_data.get('blocked_tasks_count', 0)
        risk_multiplier += blocked_count * 0.1
        
        # Complex tasks add 5% delay each
        complex_count = project_data.get('high_complexity_count', 0)
        risk_multiplier += complex_count * 0.05
        
        # Small teams have higher variance
        team_size = project_data.get('team_size', 1)
        if team_size < 3:
            risk_multiplier += 0.15
        
        adjusted_weeks = base_weeks * risk_multiplier
        
        # Generate simple confidence intervals
        confidence_range = adjusted_weeks * 0.3  # ±30%
        
        predicted_date = datetime.now() + timedelta(weeks=adjusted_weeks)
        p50_date = predicted_date
        p90_date = datetime.now() + timedelta(weeks=adjusted_weeks + confidence_range)
        p10_date = datetime.now() + timedelta(weeks=max(adjusted_weeks - confidence_range, 1))
        
        risk_factors = []
        if blocked_count > 0:
            risk_factors.append(f"{blocked_count} blocked tasks")
        if complex_count > 2:
            risk_factors.append(f"{complex_count} high-complexity tasks")
        if team_size < 3:
            risk_factors.append("Small team size increases variance")
        
        return {
            'predicted_completion_date': predicted_date.isoformat(),
            'predicted_weeks_remaining': float(adjusted_weeks),
            'confidence_intervals': {
                'p10': p10_date.isoformat(),
                'p50': p50_date.isoformat(),
                'p90': p90_date.isoformat()
            },
            'probability_on_time': None,
            'risk_factors': risk_factors,
            'model_confidence': 0.60,
            'note': 'Heuristic prediction (model not trained)'
        }
    
    def _monte_carlo_simulation(
        self,
        project_data: Dict,
        n_simulations: int = 1000
    ) -> Dict:
        """
        Run Monte Carlo simulation for confidence intervals
        
        **Process:**
        1. Simulate velocity variations week-by-week
        2. Account for random blockers
        3. Generate distribution of completion dates
        4. Extract percentiles
        """
        logger.info(f"🎲 Running {n_simulations} Monte Carlo simulations...")
        
        remaining_points = project_data.get('remaining_story_points', 0)
        avg_velocity = project_data.get('avg_weekly_velocity', 1)
        velocity_std = project_data.get('velocity_std', avg_velocity * 0.2)
        
        simulations = []
        
        for i in range(n_simulations):
            weeks = 0
            points_left = remaining_points
            
            while points_left > 0 and weeks < 104:  # Max 2 years
                # Random velocity with normal distribution
                week_velocity = max(
                    np.random.normal(avg_velocity, velocity_std),
                    0.1  # Minimum velocity
                )
                
                # 5% chance of blocker reducing velocity by 50%
                if np.random.random() < 0.05:
                    week_velocity *= 0.5
                
                points_left -= week_velocity
                weeks += 1
            
            simulations.append(weeks)
        
        simulations = np.array(simulations)
        
        logger.info(f"✅ Monte Carlo complete. Mean: {simulations.mean():.1f} weeks")
        
        return {
            'simulations': simulations,
            'mean': simulations.mean(),
            'p10': datetime.now() + timedelta(weeks=np.percentile(simulations, 10)),
            'p50': datetime.now() + timedelta(weeks=np.percentile(simulations, 50)),
            'p90': datetime.now() + timedelta(weeks=np.percentile(simulations, 90))
        }
    
    def _simple_confidence(self, predicted_weeks: float) -> Dict:
        """Simple confidence interval without full Monte Carlo"""
        variance = predicted_weeks * 0.25  # ±25%
        
        return {
            'simulations': np.array([predicted_weeks]),
            'mean': predicted_weeks,
            'p10': datetime.now() + timedelta(weeks=max(predicted_weeks - variance, 1)),
            'p50': datetime.now() + timedelta(weeks=predicted_weeks),
            'p90': datetime.now() + timedelta(weeks=predicted_weeks + variance)
        }
    
    def _identify_risk_factors(self, project_data: Dict) -> List[str]:
        """Identify specific risk factors affecting timeline"""
        risks = []
        
        # Blockers
        blocked = project_data.get('blocked_tasks_count', 0)
        if blocked > 0:
            risks.append(f"{blocked} blocked task{'s' if blocked > 1 else ''}")
        
        # Complexity
        complex = project_data.get('high_complexity_count', 0)
        if complex > 2:
            risks.append(f"{complex} high-complexity tasks")
        
        # Team size
        team_size = project_data.get('team_size', 1)
        if team_size < 3:
            risks.append("Small team (higher variability)")
        
        # Velocity trend
        velocity_std = project_data.get('velocity_std', 0)
        avg_velocity = project_data.get('avg_weekly_velocity', 1)
        if velocity_std > avg_velocity * 0.4:
            risks.append("High velocity variance (inconsistent pace)")
        
        # Stale tasks
        avg_age = project_data.get('avg_task_age_days', 0)
        if avg_age > 14:
            risks.append(f"Tasks aging ({avg_age:.0f} days avg)")
        
        return risks
    
    def _calculate_probability(
        self,
        simulations: np.ndarray,
        target_date: datetime
    ) -> float:
        """Calculate probability of meeting target date"""
        if target_date is None:
            return None
        
        target_weeks = (target_date - datetime.now()).days / 7
        probability = (simulations <= target_weeks).mean()
        
        return round(probability, 2)
    
    def train(self, training_data: pd.DataFrame):
        """
        Train the model on historical project data
        
        **Required columns:**
        - Features: All feature_names
        - Target: actual_weeks_taken
        """
        try:
            logger.info(f"🎓 Training model on {len(training_data)} projects...")
            
            # Extract features and target
            X = training_data[self.feature_names].values
            y = training_data['actual_weeks_taken'].values
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train model
            self.model.fit(X_scaled, y)
            
            # Mark as trained
            self.is_trained = True
            
            # Calculate training score
            train_score = self.model.score(X_scaled, y)
            
            logger.success(f"✅ Model trained. R² score: {train_score:.3f}")
            
            return {
                'status': 'success',
                'samples': len(training_data),
                'r2_score': train_score
            }
            
        except Exception as e:
            logger.error(f"❌ Training failed: {e}")
            raise
    
    def save(self, path: str):
        """Save model to disk"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            with open(path, 'wb') as f:
                pickle.dump({
                    'model': self.model,
                    'scaler': self.scaler,
                    'is_trained': self.is_trained,
                    'feature_names': self.feature_names
                }, f)
            logger.success(f"✅ Model saved to {path}")
        except Exception as e:
            logger.error(f"❌ Failed to save model: {e}")
            raise
    
    def load(self, path: str):
        """Load model from disk"""
        try:
            with open(path, 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.scaler = data['scaler']
                self.is_trained = data['is_trained']
                self.feature_names = data['feature_names']
            logger.success(f"✅ Model loaded from {path}")
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            raise
