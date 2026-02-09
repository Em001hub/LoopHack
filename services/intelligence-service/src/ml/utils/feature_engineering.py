"""
Feature Engineering Utilities
Transform raw data into ML features
"""

import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime
from loguru import logger
from collections import Counter


class FeatureEngineer:
    """
    Feature engineering for project intelligence ML models
    
    **Features extracted:**
    - Temporal features (time-based patterns)
    - Aggregation features (counts, sums, averages)
    - Trend features (velocity, sentiment trends)
    - Categorical features (one-hot encoding)
    - Interaction features (combinations)
    """
    
    def __init__(self):
        self.feature_names = []
        self.categorical_mappings = {}
    
    def extract_timeline_features(self, project_data: Dict) -> np.ndarray:
        """
        Extract features for timeline prediction
        
        **Returns:**
        Feature vector as numpy array
        """
        logger.info("🔧 Extracting timeline features")
        
        features = []
        feature_names = []
        
        # Basic project metrics
        features.append(project_data.get('remaining_story_points', 0))
        feature_names.append('remaining_story_points')
        
        features.append(project_data.get('avg_weekly_velocity', 1))
        feature_names.append('avg_weekly_velocity')
        
        features.append(project_data.get('velocity_std', 0))
        feature_names.append('velocity_std')
        
        features.append(project_data.get('team_size', 1))
        feature_names.append('team_size')
        
        # Risk indicators
        features.append(project_data.get('blocked_tasks_count', 0))
        feature_names.append('blocked_tasks_count')
        
        features.append(project_data.get('high_complexity_count', 0))
        feature_names.append('high_complexity_count')
        
        features.append(project_data.get('avg_task_age_days', 0))
        feature_names.append('avg_task_age_days')
        
        # Team experience
        features.append(project_data.get('team_experience_score', 0.5))
        feature_names.append('team_experience_score')
        
        # Derived features
        
        # Velocity coefficient of variation
        if project_data.get('avg_weekly_velocity', 0) > 0:
            cv = project_data.get('velocity_std', 0) / project_data.get('avg_weekly_velocity', 1)
        else:
            cv = 0
        features.append(cv)
        feature_names.append('velocity_cv')
        
        # Work per team member
        if project_data.get('team_size', 0) > 0:
            work_per_member = project_data.get('remaining_story_points', 0) / project_data.get('team_size', 1)
        else:
            work_per_member = 0
        features.append(work_per_member)
        feature_names.append('work_per_member')
        
        # Blocker ratio
        total_tasks = project_data.get('remaining_tasks', 0)
        if total_tasks > 0:
            blocker_ratio = project_data.get('blocked_tasks_count', 0) / total_tasks
        else:
            blocker_ratio = 0
        features.append(blocker_ratio)
        feature_names.append('blocker_ratio')
        
        # Complexity ratio
        if total_tasks > 0:
            complexity_ratio = project_data.get('high_complexity_count', 0) / total_tasks
        else:
            complexity_ratio = 0
        features.append(complexity_ratio)
        feature_names.append('complexity_ratio')
        
        # Time-based features
        
        # Days since project start
        if project_data.get('project_start_date'):
            try:
                start_date = datetime.fromisoformat(project_data['project_start_date'])
                days_elapsed = (datetime.now() - start_date).days
            except:
                days_elapsed = 0
        else:
            days_elapsed = 0
        features.append(days_elapsed)
        feature_names.append('days_elapsed')
        
        # Velocity trend
        velocity_trend = project_data.get('velocity_trend', 0)
        features.append(velocity_trend)
        feature_names.append('velocity_trend')
        
        self.feature_names = feature_names
        
        logger.info(f"✅ Extracted {len(features)} features")
        
        return np.array(features).reshape(1, -1)
    
    def extract_velocity_features(self, velocity_history: List[float]) -> Dict[str, float]:
        """
        Extract features from velocity time series
        
        **Features:**
        - Statistical measures (mean, std, min, max)
        - Trends (increasing/decreasing)
        - Volatility
        - Recent vs historical comparison
        """
        if not velocity_history:
            return {
                'velocity_mean': 0,
                'velocity_std': 0,
                'velocity_min': 0,
                'velocity_max': 0,
                'velocity_trend': 0,
                'velocity_volatility': 0
            }
        
        features = {}
        
        velocity_array = np.array(velocity_history)
        
        # Basic statistics
        features['velocity_mean'] = float(np.mean(velocity_array))
        features['velocity_std'] = float(np.std(velocity_array))
        features['velocity_min'] = float(np.min(velocity_array))
        features['velocity_max'] = float(np.max(velocity_array))
        features['velocity_median'] = float(np.median(velocity_array))
        
        # Trend (linear regression slope)
        if len(velocity_history) > 1:
            x = np.arange(len(velocity_history))
            slope = np.polyfit(x, velocity_array, 1)[0]
            features['velocity_trend'] = float(slope)
        else:
            features['velocity_trend'] = 0
        
        # Volatility (coefficient of variation)
        if features['velocity_mean'] > 0:
            features['velocity_volatility'] = features['velocity_std'] / features['velocity_mean']
        else:
            features['velocity_volatility'] = 0
        
        # Recent vs historical
        if len(velocity_history) >= 4:
            recent_avg = np.mean(velocity_array[-2:])  # Last 2 weeks
            historical_avg = np.mean(velocity_array[:-2])  # Before last 2 weeks
            
            if historical_avg > 0:
                features['velocity_recent_vs_historical'] = recent_avg / historical_avg
            else:
                features['velocity_recent_vs_historical'] = 1.0
        else:
            features['velocity_recent_vs_historical'] = 1.0
        
        return features
    
    def extract_team_features(self, team_data: List[Dict]) -> Dict[str, float]:
        """
        Extract team composition features
        
        **Features:**
        - Team size
        - Experience distribution
        - Skill diversity
        - Seniority distribution
        """
        features = {}
        
        features['team_size'] = len(team_data)
        
        if not team_data:
            return features
        
        # Experience levels
        experience_scores = [member.get('experience_score', 0.5) for member in team_data]
        features['avg_experience'] = float(np.mean(experience_scores))
        features['min_experience'] = float(np.min(experience_scores))
        features['max_experience'] = float(np.max(experience_scores))
        
        # Seniority distribution
        seniority_counts = Counter([member.get('seniority', 'mid') for member in team_data])
        features['senior_count'] = seniority_counts.get('senior', 0) + seniority_counts.get('staff', 0)
        features['junior_count'] = seniority_counts.get('junior', 0)
        features['mid_count'] = seniority_counts.get('mid', 0)
        
        # Skill diversity
        all_skills = []
        for member in team_data:
            all_skills.extend(member.get('skills', []))
        features['unique_skills'] = len(set(all_skills))
        
        # Average skills per person
        skills_per_person = [len(member.get('skills', [])) for member in team_data]
        features['avg_skills_per_person'] = float(np.mean(skills_per_person)) if skills_per_person else 0
        
        return features
    
    def create_interaction_features(
        self,
        features_dict: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Create interaction features (products of existing features)
        
        **Example:**
        - team_size * avg_experience = total_team_capacity
        - remaining_points * complexity_ratio = adjusted_work
        """
        interaction_features = {}
        
        # Team capacity
        if 'team_size' in features_dict and 'avg_experience' in features_dict:
            interaction_features['team_capacity'] = (
                features_dict['team_size'] * features_dict['avg_experience']
            )
        
        # Adjusted workload
        if 'remaining_story_points' in features_dict and 'complexity_ratio' in features_dict:
            interaction_features['adjusted_workload'] = (
                features_dict['remaining_story_points'] * (1 + features_dict.get('complexity_ratio', 0))
            )
        
        # Risk-adjusted velocity
        if 'avg_weekly_velocity' in features_dict and 'blocker_ratio' in features_dict:
            interaction_features['risk_adjusted_velocity'] = (
                features_dict['avg_weekly_velocity'] * (1 - features_dict.get('blocker_ratio', 0))
            )
        
        return interaction_features
    
    def extract_all_features(
        self,
        project_data: Dict,
        team_data: List[Dict],
        velocity_history: List[float]
    ) -> Dict[str, float]:
        """
        Extract all features for a project
        
        **Returns:**
        Complete feature dictionary
        """
        logger.info("🔧 Extracting all features")
        
        all_features = {}
        
        # Basic project features
        basic_features = {
            'remaining_story_points': project_data.get('remaining_story_points', 0),
            'remaining_tasks': project_data.get('remaining_tasks', 0),
            'blocked_tasks_count': project_data.get('blocked_tasks_count', 0),
            'high_complexity_count': project_data.get('high_complexity_count', 0),
            'avg_task_age_days': project_data.get('avg_task_age_days', 0)
        }
        all_features.update(basic_features)
        
        # Velocity features
        velocity_features = self.extract_velocity_features(velocity_history)
        all_features.update(velocity_features)
        
        # Team features
        team_features = self.extract_team_features(team_data)
        all_features.update(team_features)
        
        # Interaction features
        interaction_features = self.create_interaction_features(all_features)
        all_features.update(interaction_features)
        
        logger.info(f"✅ Extracted {len(all_features)} total features")
        
        return all_features
