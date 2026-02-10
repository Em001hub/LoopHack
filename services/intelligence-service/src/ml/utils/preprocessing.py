"""
Data Preprocessing Utilities
Clean and prepare data for ML models
"""

import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime
from loguru import logger


class DataPreprocessor:
    """
    Preprocess raw data for ML models
    
    **Operations:**
    - Handle missing values
    - Remove outliers
    - Validate data types
    - Clean text
    - Format timestamps
    """
    
    def __init__(self):
        self.imputation_values = {}
    
    def clean_project_data(self, project_data: Dict) -> Dict:
        """
        Clean and validate project data
        
        **Cleaning operations:**
        - Fill missing values
        - Ensure non-negative numbers
        - Validate ranges
        """
        logger.info("🧹 Cleaning project data")
        
        cleaned = project_data.copy()
        
        # Ensure numeric fields are present and valid
        numeric_fields = {
            'remaining_story_points': 0,
            'remaining_tasks': 0,
            'avg_weekly_velocity': 1,
            'velocity_std': 0,
            'team_size': 1,
            'blocked_tasks_count': 0,
            'high_complexity_count': 0,
            'avg_task_age_days': 0,
            'team_experience_score': 0.5
        }
        
        for field, default_value in numeric_fields.items():
            if field not in cleaned or cleaned[field] is None:
                cleaned[field] = default_value
                logger.debug(f"Filled missing value for {field} with {default_value}")
            
            # Ensure non-negative (except velocity trend)
            if field != 'velocity_trend':
                cleaned[field] = max(0, float(cleaned[field]))
        
        # Validate ranges
        if cleaned['team_experience_score'] > 1:
            cleaned['team_experience_score'] = 1.0
        
        if cleaned['team_size'] < 1:
            cleaned['team_size'] = 1
        
        # Ensure velocity_std is not greater than velocity mean
        if cleaned['velocity_std'] > cleaned['avg_weekly_velocity']:
            cleaned['velocity_std'] = cleaned['avg_weekly_velocity'] * 0.5
        
        logger.info("✅ Project data cleaned")
        
        return cleaned
    
    def remove_outliers(
        self,
        data: np.ndarray,
        method: str = 'iqr',
        threshold: float = 1.5
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Remove outliers from data
        
        **Methods:**
        - iqr: Interquartile range method
        - zscore: Z-score method
        
        **Returns:**
        (cleaned_data, outlier_mask)
        """
        logger.info(f"🎯 Removing outliers (method: {method})")
        
        if method == 'iqr':
            q1 = np.percentile(data, 25)
            q3 = np.percentile(data, 75)
            iqr = q3 - q1
            
            lower_bound = q1 - threshold * iqr
            upper_bound = q3 + threshold * iqr
            
            mask = (data >= lower_bound) & (data <= upper_bound)
        
        elif method == 'zscore':
            mean = np.mean(data)
            std = np.std(data)
            
            if std > 0:
                z_scores = np.abs((data - mean) / std)
                mask = z_scores < threshold
            else:
                mask = np.ones(len(data), dtype=bool)
        
        else:
            raise ValueError(f"Unknown method: {method}")
        
        cleaned_data = data[mask]
        
        outliers_removed = len(data) - len(cleaned_data)
        if len(data) > 0:
            logger.info(f"✅ Removed {outliers_removed} outliers ({outliers_removed/len(data)*100:.1f}%)")
        
        return cleaned_data, mask
    
    def validate_velocity_history(
        self,
        velocity_history: List[float]
    ) -> List[float]:
        """
        Validate and clean velocity history
        
        **Validation:**
        - Remove negative values
        - Remove extreme outliers
        - Ensure reasonable values
        """
        if not velocity_history:
            return []
        
        cleaned = []
        
        for velocity in velocity_history:
            # Remove negative or zero
            if velocity <= 0:
                continue
            
            # Remove unreasonably high values (> 1000 points/week)
            if velocity > 1000:
                continue
            
            cleaned.append(velocity)
        
        # If we removed too many, fill with median
        if len(cleaned) < len(velocity_history) * 0.5:
            logger.warning("Too many invalid velocity values, using median")
            if cleaned:
                median_velocity = np.median(cleaned)
                cleaned = [median_velocity] * max(3, len(cleaned))
        
        return cleaned
    
    def clean_text(self, text: str) -> str:
        """
        Clean text data
        
        **Operations:**
        - Remove extra whitespace
        - Normalize case
        """
        if not text:
            return ""
        
        import re
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def standardize_timestamps(
        self,
        timestamps: List
    ) -> List[datetime]:
        """
        Standardize timestamp formats
        
        **Accepts:**
        - datetime objects
        - ISO format strings
        - Unix timestamps
        """
        standardized = []
        
        for ts in timestamps:
            if isinstance(ts, datetime):
                standardized.append(ts)
            
            elif isinstance(ts, str):
                try:
                    # Try ISO format
                    dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                    standardized.append(dt)
                except:
                    logger.warning(f"Could not parse timestamp: {ts}")
                    standardized.append(datetime.now())
            
            elif isinstance(ts, (int, float)):
                # Unix timestamp
                try:
                    dt = datetime.fromtimestamp(ts)
                    standardized.append(dt)
                except:
                    logger.warning(f"Invalid unix timestamp: {ts}")
                    standardized.append(datetime.now())
            
            else:
                logger.warning(f"Unknown timestamp type: {type(ts)}")
                standardized.append(datetime.now())
        
        return standardized
    
    def normalize_features(
        self,
        features: np.ndarray,
        method: str = 'standard'
    ) -> np.ndarray:
        """
        Normalize features
        
        **Methods:**
        - standard: (x - mean) / std
        - minmax: (x - min) / (max - min)
        """
        if method == 'standard':
            mean = np.mean(features, axis=0)
            std = np.std(features, axis=0)
            std[std == 0] = 1  # Avoid division by zero
            return (features - mean) / std
        
        elif method == 'minmax':
            min_val = np.min(features, axis=0)
            max_val = np.max(features, axis=0)
            range_val = max_val - min_val
            range_val[range_val == 0] = 1
            return (features - min_val) / range_val
        
        else:
            raise ValueError(f"Unknown normalization method: {method}")
