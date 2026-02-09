"""
Monte Carlo Simulation Engine
Runs probabilistic simulations for timeline forecasting
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from loguru import logger


class MonteCarloSimulator:
    """
    Advanced Monte Carlo simulation for project predictions
    
    **Simulates:**
    - Random velocity variations
    - Blocker occurrences
    - Team changes
    - Scope changes
    
    **Outputs:**
    - Probability distribution of completion dates
    - Confidence intervals
    - Risk scenarios
    """
    
    def __init__(self, n_simulations: int = 1000):
        self.n_simulations = n_simulations
        logger.info(f"🎲 Monte Carlo simulator initialized ({n_simulations} runs)")
    
    def simulate_project_timeline(
        self,
        project_data: Dict,
        scenario_params: Optional[Dict] = None
    ) -> Dict:
        """
        Run Monte Carlo simulation for project timeline
        
        **Parameters:**
        project_data: Current project state
        scenario_params: What-if scenario parameters
        
        **Returns:**
        - Distribution of completion dates
        - Percentiles (p10, p50, p90)
        - Probability of meeting deadline
        - Risk breakdown
        """
        logger.info(f"🎲 Running {self.n_simulations} simulations...")
        
        # Extract base parameters
        remaining_points = project_data.get('remaining_story_points', 0)
        avg_velocity = project_data.get('avg_weekly_velocity', 1)
        velocity_std = project_data.get('velocity_std', avg_velocity * 0.2)
        team_size = project_data.get('team_size', 1)
        
        # Apply scenario modifications
        if scenario_params:
            remaining_points, avg_velocity, velocity_std, team_size = self._apply_scenario(
                remaining_points, avg_velocity, velocity_std, team_size, scenario_params
            )
        
        # Run simulations
        completion_weeks = []
        blocker_counts = []
        
        for sim in range(self.n_simulations):
            weeks, blockers = self._run_single_simulation(
                remaining_points,
                avg_velocity,
                velocity_std,
                team_size
            )
            completion_weeks.append(weeks)
            blocker_counts.append(blockers)
        
        completion_weeks = np.array(completion_weeks)
        
        # Calculate statistics
        result = {
            'simulation_count': self.n_simulations,
            'predicted_weeks': {
                'mean': float(np.mean(completion_weeks)),
                'median': float(np.median(completion_weeks)),
                'std': float(np.std(completion_weeks)),
                'min': float(np.min(completion_weeks)),
                'max': float(np.max(completion_weeks))
            },
            'percentiles': {
                'p10': float(np.percentile(completion_weeks, 10)),
                'p25': float(np.percentile(completion_weeks, 25)),
                'p50': float(np.percentile(completion_weeks, 50)),
                'p75': float(np.percentile(completion_weeks, 75)),
                'p90': float(np.percentile(completion_weeks, 90))
            },
            'completion_dates': {
                'p10': (datetime.now() + timedelta(weeks=np.percentile(completion_weeks, 10))).isoformat(),
                'p50': (datetime.now() + timedelta(weeks=np.percentile(completion_weeks, 50))).isoformat(),
                'p90': (datetime.now() + timedelta(weeks=np.percentile(completion_weeks, 90))).isoformat()
            },
            'risk_analysis': {
                'avg_blockers_encountered': float(np.mean(blocker_counts)),
                'probability_major_delay': float((completion_weeks > np.median(completion_weeks) * 1.5).mean()),
                'scenarios_exceeding_year': int((completion_weeks > 52).sum())
            },
            'distribution': self._create_histogram(completion_weeks),
            'scenario_params': scenario_params or {}
        }
        
        # Calculate probability of meeting target if provided
        target_date = project_data.get('target_date')
        if target_date:
            target_weeks = (datetime.fromisoformat(target_date) - datetime.now()).days / 7
            probability = (completion_weeks <= target_weeks).mean()
            result['probability_on_time'] = round(probability, 2)
        
        logger.success(f"✅ Simulation complete. Median: {result['predicted_weeks']['median']:.1f} weeks")
        
        return result
    
    def _run_single_simulation(
        self,
        remaining_points: float,
        avg_velocity: float,
        velocity_std: float,
        team_size: int
    ) -> tuple:
        """Run a single simulation iteration"""
        weeks = 0
        points_left = remaining_points
        blockers_hit = 0
        
        while points_left > 0 and weeks < 104:  # Max 2 years
            # Random velocity with normal distribution
            week_velocity = max(
                np.random.normal(avg_velocity, velocity_std),
                0.1  # Minimum velocity
            )
            
            # Random blocker probability (5% per week base)
            blocker_prob = 0.05
            
            # Smaller teams have higher blocker impact
            if team_size < 3:
                blocker_prob *= 1.5
            
            if np.random.random() < blocker_prob:
                # Blocker reduces velocity by 30-70%
                reduction = np.random.uniform(0.3, 0.7)
                week_velocity *= (1 - reduction)
                blockers_hit += 1
            
            # Rare critical blocker (1% chance, stops progress for a week)
            if np.random.random() < 0.01:
                week_velocity = 0
                blockers_hit += 1
            
            # Add some random positive variance too (good weeks)
            if np.random.random() < 0.1:  # 10% chance of good week
                week_velocity *= 1.2
            
            points_left -= week_velocity
            weeks += 1
        
        return weeks, blockers_hit
    
    def _apply_scenario(
        self,
        remaining_points: float,
        avg_velocity: float,
        velocity_std: float,
        team_size: int,
        scenario_params: Dict
    ) -> tuple:
        """Apply what-if scenario modifications"""
        
        # Add developers
        if 'add_developers' in scenario_params:
            devs_added = scenario_params['add_developers']
            # Each dev adds 15% velocity after 2-week ramp-up
            avg_velocity *= (1 + devs_added * 0.15)
            team_size += devs_added
            logger.info(f"Scenario: Added {devs_added} developers")
        
        # Remove features
        if 'remove_features' in scenario_params:
            points_removed = scenario_params['remove_features']
            remaining_points -= points_removed
            logger.info(f"Scenario: Removed {points_removed} story points")
        
        # Increase QA time
        if 'increase_qa_time_pct' in scenario_params:
            qa_increase = scenario_params['increase_qa_time_pct'] / 100
            avg_velocity *= (1 - qa_increase * 0.5)  # QA reduces velocity
            logger.info(f"Scenario: Increased QA time by {scenario_params['increase_qa_time_pct']}%")
        
        # Reduce scope
        if 'reduce_scope_pct' in scenario_params:
            scope_reduction = scenario_params['reduce_scope_pct'] / 100
            remaining_points *= (1 - scope_reduction)
            logger.info(f"Scenario: Reduced scope by {scenario_params['reduce_scope_pct']}%")
        
        return remaining_points, avg_velocity, velocity_std, team_size
    
    def _create_histogram(self, data: np.ndarray, bins: int = 20) -> Dict:
        """Create histogram data for visualization"""
        counts, bin_edges = np.histogram(data, bins=bins)
        
        return {
            'bins': [float(x) for x in bin_edges[:-1]],
            'counts': [int(x) for x in counts],
            'bin_width': float(bin_edges[1] - bin_edges[0])
        }
    
    def compare_scenarios(
        self,
        project_data: Dict,
        scenarios: List[Dict]
    ) -> Dict:
        """
        Compare multiple what-if scenarios
        
        **Returns:**
        Side-by-side comparison of all scenarios
        """
        logger.info(f"📊 Comparing {len(scenarios)} scenarios...")
        
        results = {}
        
        # Baseline (no changes)
        baseline = self.simulate_project_timeline(project_data, scenario_params=None)
        results['baseline'] = baseline
        
        # Each scenario
        for i, scenario in enumerate(scenarios):
            scenario_name = scenario.get('name', f"Scenario {i+1}")
            scenario_result = self.simulate_project_timeline(project_data, scenario_params=scenario)
            results[scenario_name] = scenario_result
        
        # Create comparison summary
        comparison = {
            'scenarios': results,
            'comparison_table': self._create_comparison_table(results),
            'recommendation': self._recommend_best_scenario(results)
        }
        
        logger.success(f"✅ Comparison complete")
        
        return comparison
    
    def _create_comparison_table(self, results: Dict) -> List[Dict]:
        """Create comparison table"""
        table = []
        
        for name, result in results.items():
            table.append({
                'scenario': name,
                'median_weeks': result['predicted_weeks']['median'],
                'p90_weeks': result['percentiles']['p90'],
                'probability_on_time': result.get('probability_on_time'),
                'risk_level': 'High' if result['predicted_weeks']['std'] > 10 else 'Medium' if result['predicted_weeks']['std'] > 5 else 'Low'
            })
        
        return table
    
    def _recommend_best_scenario(self, results: Dict) -> str:
        """Recommend best scenario based on results"""
        # Simple logic: scenario with highest probability of on-time delivery
        best_scenario = None
        best_prob = 0
        
        for name, result in results.items():
            prob = result.get('probability_on_time', 0) or 0
            if prob > best_prob:
                best_prob = prob
                best_scenario = name
        
        if best_scenario:
            return f"Recommend: {best_scenario} ({best_prob:.0%} on-time probability)"
        else:
            return "No clear recommendation"
