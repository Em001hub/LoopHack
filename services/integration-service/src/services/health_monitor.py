from typing import List, Dict, Any
from src.models.unified import Task, Event
from datetime import datetime

class HealthMonitor:
    def __init__(self):
        pass

    def calculate_health_score(
        self, 
        tasks: List[Task], 
        events: List[Event],
        avg_velocity: float
    ) -> Dict[str, Any]:
        """
        Calculate a multi-dimensional health score for a project.
        Dimensions:
        - Velocity (lagging)
        - Blocker Density (leading)
        - Communication Quality (leading)
        - Stale Task Rate (leading)
        """
        
        # 1. Velocity Score
        completed_points = sum(t.story_points or 1 for t in tasks if t.status == 'done')
        velocity_ratio = min(completed_points / max(avg_velocity, 1), 1.2)
        velocity_score = velocity_ratio * 100

        # 2. Blocker Score
        blockers = [t for t in tasks if t.metadata.get('is_blocked')]
        blocker_ratio = len(blockers) / max(len(tasks), 1)
        blocker_score = max(100 - (blocker_ratio * 200), 0)  # 50% blockers = 0 score

        # 3. Communication Score
        messages = [e for e in events if e.event_type == 'slack_message']
        comm_density = len(messages) / max(len(tasks), 1)
        # Assuming 5-10 messages per task is healthy
        comm_score = min(comm_density / 5, 1.0) * 100

        # 4. Stale Task Score
        # (Assuming stale means not updated in 3 days)
        # This is simplified for the example
        stale_tasks = [t for t in tasks if (datetime.now() - t.updated_at).days > 3]
        stale_ratio = len(stale_tasks) / max(len(tasks), 1)
        stale_score = max(100 - (stale_ratio * 150), 0)

        # Aggregate weighted score
        weights = {
            "velocity": 0.4,
            "blocker": 0.3,
            "communication": 0.1,
            "stale": 0.2
        }

        overall_score = (
            velocity_score * weights["velocity"] +
            blocker_score * weights["blocker"] +
            comm_score * weights["communication"] +
            stale_score * weights["stale"]
        )

        return {
            "overall_score": round(overall_score, 2),
            "dimensions": {
                "velocity": round(velocity_score, 2),
                "blockers": round(blocker_score, 2),
                "communication": round(comm_score, 2),
                "stale_tasks": round(stale_score, 2)
            },
            "interpretation": self._interpret_score(overall_score)
        }

    def _interpret_score(self, score: float) -> str:
        if score > 80: return "Healthy"
        if score > 60: return "At Risk"
        if score > 40: return "Critical"
        return "Severe"
