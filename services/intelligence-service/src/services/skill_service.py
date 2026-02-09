"""
Skill Service
Orchestrates skill extraction and team skill analysis
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import Dict, List, Optional
from loguru import logger
from datetime import datetime, timedelta

from src.ml.models.skill_extractor import SkillExtractor


class SkillService:
    """
    Service layer for skill extraction and analysis
    Handles data fetching and skill model orchestration
    """
    
    def __init__(self):
        self.extractor = SkillExtractor()
    
    async def extract_user_skills(
        self,
        db: AsyncSession,
        user_id: str,
        days: int = 90
    ) -> Dict:
        """
        Extract skills from all user activity sources
        
        **Sources:**
        - GitHub commits and PRs
        - Slack messages
        - Jira task assignments
        """
        logger.info(f"🔍 Extracting skills for {user_id} (last {days} days)")
        
        # Fetch GitHub activity
        github_events = await self._fetch_github_activity(db, user_id, days)
        
        # Fetch Slack messages
        slack_messages = await self._fetch_slack_messages(db, user_id, days)
        
        # Extract skills from GitHub
        github_skills = self.extractor.extract_skills_from_github(user_id, github_events, days)
        
        # Extract skills from Slack
        slack_skills = self.extractor.extract_skills_from_slack(user_id, slack_messages)
        
        # Combine skills
        combined_skills = self.extractor.combine_skill_sources(
            github_skills=github_skills,
            slack_skills=slack_skills
        )
        
        # Cache the results
        await self._cache_skills(db, user_id, combined_skills)
        
        logger.success(f"✅ Extracted {len(combined_skills.get('technical_skills', []))} skills")
        
        return combined_skills
    
    async def _fetch_github_activity(
        self,
        db: AsyncSession,
        user_id: str,
        days: int
    ) -> List[Dict]:
        """Fetch GitHub events from database"""
        query = text("""
            SELECT 
                timestamp,
                event_type,
                metadata
            FROM github_events
            WHERE user_id = :user_id
              AND timestamp > NOW() - INTERVAL ':days days'
            ORDER BY timestamp DESC
        """)
        
        result = await db.execute(query, {'user_id': user_id, 'days': days})
        rows = result.fetchall()
        
        return [
            {
                'timestamp': row[0].isoformat(),
                'event_type': row[1],
                'metadata': row[2] or {}
            }
            for row in rows
        ]
    
    async def _fetch_slack_messages(
        self,
        db: AsyncSession,
        user_id: str,
        days: int
    ) -> List[Dict]:
        """Fetch Slack messages from database"""
        query = text("""
            SELECT 
                timestamp,
                channel_id,
                metadata
            FROM slack_messages
            WHERE user_id = :user_id
              AND timestamp > NOW() - INTERVAL ':days days'
            ORDER BY timestamp DESC
        """)
        
        result = await db.execute(query, {'user_id': user_id, 'days': days})
        rows = result.fetchall()
        
        return [
            {
                'timestamp': row[0].isoformat(),
                'channel_id': row[1],
                'metadata': row[2] or {}
            }
            for row in rows
        ]
    
    async def _cache_skills(
        self,
        db: AsyncSession,
        user_id: str,
        skills: Dict
    ):
        """Cache skill profile in database"""
        try:
            query = text("""
                INSERT INTO user_skills (
                    user_id,
                    skill_profile,
                    updated_at
                ) VALUES (
                    :user_id,
                    :skill_profile,
                    NOW()
                )
                ON CONFLICT (user_id)
                DO UPDATE SET
                    skill_profile = :skill_profile,
                    updated_at = NOW()
            """)
            
            await db.execute(query, {
                'user_id': user_id,
                'skill_profile': str(skills)
            })
            
            await db.commit()
            logger.info("✅ Skills cached")
            
        except Exception as e:
            logger.error(f"Failed to cache skills: {e}")
            await db.rollback()
    
    async def get_cached_skills(
        self,
        db: AsyncSession,
        user_id: str
    ) -> Optional[Dict]:
        """Retrieve cached skill profile"""
        query = text("""
            SELECT skill_profile, updated_at
            FROM user_skills
            WHERE user_id = :user_id
        """)
        
        result = await db.execute(query, {'user_id': user_id})
        row = result.fetchone()
        
        if not row:
            return None
        
        # Parse skill profile (would use JSON in production)
        return eval(row[0])  # In production, use json.loads
    
    async def match_task_to_user(
        self,
        db: AsyncSession,
        user_id: str,
        task_requirements: Dict
    ) -> Dict:
        """Match user skills to task requirements"""
        # Get user skills
        user_skills = await self.get_cached_skills(db, user_id)
        
        if not user_skills:
            # Extract skills if not cached
            user_skills = await self.extract_user_skills(db, user_id)
        
        # Use extractor to match
        match = self.extractor.recommend_task_match(user_skills, task_requirements)
        
        return match
    
    async def generate_team_skill_matrix(
        self,
        db: AsyncSession,
        project_id: str
    ) -> Dict:
        """Generate skill matrix for entire team"""
        logger.info(f"👥 Generating skill matrix for project: {project_id}")
        
        # Get team members
        team_query = text("""
            SELECT DISTINCT assignee_id
            FROM tasks
            WHERE project_id = :project_id
              AND assignee_id IS NOT NULL
        """)
        
        result = await db.execute(team_query, {'project_id': project_id})
        team_members = [row[0] for row in result.fetchall()]
        
        # Get skills for each member
        team_skills = {}
        all_skills = set()
        
        for user_id in team_members:
            skills = await self.get_cached_skills(db, user_id)
            if skills:
                team_skills[user_id] = skills
                # Collect all unique skills
                for skill in skills.get('technical_skills', []):
                    all_skills.add(skill['name'])
        
        # Analyze coverage
        skill_coverage = {}
        for skill in all_skills:
            experts = []
            for user_id, skills in team_skills.items():
                for s in skills.get('technical_skills', []):
                    if s['name'] == skill and s['proficiency'] > 0.7:
                        experts.append(user_id)
            
            skill_coverage[skill] = {
                'expert_count': len(experts),
                'experts': experts,
                'risk': 'high' if len(experts) <= 1 else 'low'
            }
        
        # Identify knowledge silos (single points of failure)
        knowledge_silos = [
            skill for skill, data in skill_coverage.items()
            if data['expert_count'] == 1
        ]
        
        matrix = {
            'project_id': project_id,
            'team_size': len(team_members),
            'team_members': team_members,
            'team_skills': team_skills,
            'skill_coverage': skill_coverage,
            'knowledge_silos': knowledge_silos,
            'total_unique_skills': len(all_skills)
        }
        
        logger.success(f"✅ Matrix: {len(team_members)} members, {len(all_skills)} skills")
        
        return matrix
    
    async def recommend_task_assignment(
        self,
        db: AsyncSession,
        task_id: str
    ) -> List[Dict]:
        """Recommend best team member for task"""
        logger.info(f"🤖 Finding assignee for task: {task_id}")
        
        # Get task details and requirements
        task_query = text("""
            SELECT project_id, metadata
            FROM tasks
            WHERE id = :task_id
        """)
        
        result = await db.execute(task_query, {'task_id': task_id})
        task_row = result.fetchone()
        
        if not task_row:
            return []
        
        project_id = task_row[0]
        task_metadata = task_row[1] or {}
        task_requirements = task_metadata.get('required_skills', {})
        
        # Get team members
        team_query = text("""
            SELECT DISTINCT assignee_id
            FROM tasks
            WHERE project_id = :project_id
              AND assignee_id IS NOT NULL
        """)
        
        result = await db.execute(team_query, {'project_id': project_id})
        team_members = [row[0] for row in result.fetchall()]
        
        # Match each team member
        recommendations = []
        for user_id in team_members:
            match = await self.match_task_to_user(db, user_id, task_requirements)
            
            recommendations.append({
                'user_id': user_id,
                'match_score': match['match_score'],
                'recommendation': match['recommendation'],
                'matched_skills': match.get('required_skills_matched', []),
                'missing_skills': match.get('required_skills_missing', [])
            })
        
        # Sort by match score
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        
        logger.success(f"✅ Top match: {recommendations[0]['user_id']} ({recommendations[0]['match_score']:.0%})")
        
        return recommendations
