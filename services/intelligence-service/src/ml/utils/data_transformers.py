"""
Custom Data Transformers for ML Pipeline
Scikit-learn compatible transformers
"""

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from typing import List, Dict, Any
from loguru import logger


class VelocityFeatureTransformer(BaseEstimator, TransformerMixin):
    """
    Transform velocity time series into statistical features
    
    **Compatible with sklearn Pipeline**
    """
    
    def __init__(self):
        self.feature_names = []
    
    def fit(self, X, y=None):
        """Fit transformer (no-op for this transformer)"""
        return self
    
    def transform(self, X):
        """
        Transform velocity history into features
        
        **Input:** List of velocity arrays
        **Output:** Feature matrix
        """
        features = []
        
        for velocity_history in X:
            if not isinstance(velocity_history, (list, np.ndarray)):
                velocity_history = []
            
            if len(velocity_history) == 0:
                # No history - use defaults
                features.append([0, 0, 0, 0, 0, 0, 0])
                continue
            
            velocity_array = np.array(velocity_history)
            
            # Statistical features
            mean = np.mean(velocity_array)
            std = np.std(velocity_array)
            min_val = np.min(velocity_array)
            max_val = np.max(velocity_array)
            median = np.median(velocity_array)
            
            # Trend (linear regression slope)
            if len(velocity_history) > 1:
                x = np.arange(len(velocity_history))
                trend = np.polyfit(x, velocity_array, 1)[0]
            else:
                trend = 0
            
            # Coefficient of variation
            cv = std / mean if mean > 0 else 0
            
            features.append([mean, std, min_val, max_val, median, trend, cv])
        
        self.feature_names = [
            'velocity_mean', 'velocity_std', 'velocity_min', 'velocity_max',
            'velocity_median', 'velocity_trend', 'velocity_cv'
        ]
        
        return np.array(features)
    
    def get_feature_names_out(self, input_features=None):
        """Return feature names"""
        return self.feature_names


class TeamCompositionTransformer(BaseEstimator, TransformerMixin):
    """
    Transform team composition data into features
    """
    
    def __init__(self):
        self.feature_names = []
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        """
        Transform team data into features
        
        **Input:** List of team member arrays
        **Output:** Feature matrix
        """
        features = []
        
        for team_data in X:
            if not isinstance(team_data, (list, np.ndarray)):
                team_data = []
            
            if len(team_data) == 0:
                features.append([0, 0, 0, 0])
                continue
            
            # Team size
            team_size = len(team_data)
            
            # Average experience (if available)
            if isinstance(team_data[0], dict):
                experience_scores = [m.get('experience', 0.5) for m in team_data]
                avg_experience = np.mean(experience_scores)
                
                # Seniority counts
                senior_count = sum(1 for m in team_data if m.get('seniority', 'mid') in ['senior', 'staff'])
                junior_count = sum(1 for m in team_data if m.get('seniority', 'mid') == 'junior')
            else:
                avg_experience = 0.5
                senior_count = 0
                junior_count = 0
            
            features.append([team_size, avg_experience, senior_count, junior_count])
        
        self.feature_names = ['team_size', 'avg_experience', 'senior_count', 'junior_count']
        
        return np.array(features)
    
    def get_feature_names_out(self, input_features=None):
        return self.feature_names


class OutlierRemovalTransformer(BaseEstimator, TransformerMixin):
    """
    Remove outliers using IQR method
    """
    
    def __init__(self, threshold=1.5):
        self.threshold = threshold
        self.lower_bounds = None
        self.upper_bounds = None
    
    def fit(self, X, y=None):
        """Calculate bounds from training data"""
        q1 = np.percentile(X, 25, axis=0)
        q3 = np.percentile(X, 75, axis=0)
        iqr = q3 - q1
        
        self.lower_bounds = q1 - self.threshold * iqr
        self.upper_bounds = q3 + self.threshold * iqr
        
        return self
    
    def transform(self, X):
        """Clip values to bounds"""
        X_clipped = np.clip(X, self.lower_bounds, self.upper_bounds)
        return X_clipped


class LogTransformer(BaseEstimator, TransformerMixin):
    """
    Apply log transformation to skewed features
    """
    
    def __init__(self, epsilon=1e-6):
        self.epsilon = epsilon
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        """Apply log(1 + x) transformation"""
        return np.log1p(X + self.epsilon)
    
    def inverse_transform(self, X):
        """Reverse transformation"""
        return np.expm1(X) - self.epsilon
