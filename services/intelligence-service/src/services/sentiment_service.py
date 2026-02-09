"""
Sentiment Service
Orchestrates sentiment analysis and team morale tracking
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import Dict, List, Optional
from loguru import logger
from datetime import datetime, timedelta

from src.ml.models.sentiment_analyzer import SentimentAnalyzer


class SentimentService:
    """
    Service layer for sentiment analysis
    Handles data fetching and sentiment model orchestration
    """
    
    def __init__(self):
        self.analyzer = SentimentAnalyzer()
    
    async def analyze_user_sentiment(
        self,
        db: AsyncSession,
        user_id: str,
        days: int = 30
    ) -> Dict:
        """
        Analyze sentiment trend for a user
        
        **Returns:**
        - Sentiment trend (improving/declining/stable)
        - Current morale level
        - Burnout risk assessment
        - Daily sentiment scores
        """
        logger.info(f"😊 Analyzing sentiment for {user_id} (last {days} days)")
        
        # Fetch user messages
        messages = await self._fetch_user_messages(db, user_id, days)
        
        if not messages:
            raise ValueError(f"No messages found for user {user_id}")
        
        # Analyze trend
        trend = self.analyzer.analyze_user_sentiment_trend(user_id, messages, days)
        
        logger.success(f"✅ Sentiment: {trend['current_sentiment']['label']}")
        
        return trend
    
    async def analyze_team_morale(
        self,
        db: AsyncSession,
        project_id: str,
        days: int = 30
    ) -> Dict:
        """
        Analyze overall team morale
        
        **Returns:**
        - Team average sentiment
        - Individual member sentiments
        - At-risk team members
        - Morale distribution
        """
        logger.info(f"👥 Analyzing team morale for project: {project_id}")
        
        # Get team members
        team_members = await self._get_team_members(db, project_id)
        
        # Fetch messages for each member
        team_messages = {}
        for user_id in team_members:
            messages = await self._fetch_user_messages(db, user_id, days)
            if messages:
                team_messages[user_id] = messages
        
        # Analyze team morale
        morale = self.analyzer.analyze_team_morale(team_messages)
        
        logger.success(f"✅ Team morale: {morale['team_morale']['label']}")
        
        return morale
    
    async def calculate_burnout_risk(
        self,
        db: AsyncSession,
        user_id: str
    ) -> Dict:
        """
        Calculate burnout risk for a specific user
        
        **Returns:**
        - Risk level (Low/Medium/High)
        - Risk score (0-100)
        - Specific indicators
        - Recommended action
        """
        logger.info(f"⚠️  Calculating burnout risk for: {user_id}")
        
        # Get user messages (last 30 days)
        messages = await self._fetch_user_messages(db, user_id, days=30)
        
        if not messages:
            return {
                'user_id': user_id,
                'level': 'Unknown',
                'score': 0,
                'indicators': ['Insufficient data'],
                'recommended_action': 'No data available for analysis'
            }
        
        # Analyze sentiment trend
        trend = self.analyzer.analyze_user_sentiment_trend(user_id, messages, days=30)
        
        # Extract burnout risk
        burnout_risk = trend.get('burnout_risk', {})
        burnout_risk['user_id'] = user_id
        
        logger.info(f"Risk: {burnout_risk.get('level', 'Unknown')}")
        
        return burnout_risk
    
    async def get_sentiment_alerts(
        self,
        db: AsyncSession,
        project_id: str
    ) -> List[Dict]:
        """
        Get active sentiment-based alerts
        
        **Alert types:**
        - High burnout risk
        - Team morale declining
        - Individual stress signals
        """
        logger.info(f"🚨 Fetching sentiment alerts for: {project_id}")
        
        alerts = []
        
        # Analyze team morale
        morale = await self.analyze_team_morale(db, project_id, days=30)
        
        # Check for at-risk members
        for member in morale.get('at_risk_members', []):
            alerts.append({
                'type': 'burnout_risk',
                'severity': member['risk_level'].lower(),
                'user_id': member['user_id'],
                'message': f"Team member at {member['risk_level']} burnout risk",
                'recommended_action': member['recommended_action'],
                'created_at': datetime.now().isoformat()
            })
        
        # Check team morale trend
        if morale['team_morale']['trend'] == 'declining':
            alerts.append({
                'type': 'team_morale_declining',
                'severity': 'medium',
                'message': 'Overall team morale is declining',
                'recommended_action': 'Schedule team retrospective or check-in',
                'created_at': datetime.now().isoformat()
            })
        
        # Check for low morale members
        if morale.get('low_morale_count', 0) > morale.get('members_analyzed', 1) * 0.3:
            alerts.append({
                'type': 'high_low_morale_ratio',
                'severity': 'high',
                'message': f"{morale['low_morale_count']} team members with low morale",
                'recommended_action': 'Investigate team issues and address concerns',
                'created_at': datetime.now().isoformat()
            })
        
        logger.info(f"Found {len(alerts)} active alerts")
        
        return alerts
    
    async def _fetch_user_messages(
        self,
        db: AsyncSession,
        user_id: str,
        days: int
    ) -> List[Dict]:
        """Fetch user messages from database"""
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
                'text': (row[2] or {}).get('text', ''),
                'metadata': row[2] or {}
            }
            for row in rows
        ]
    
    async def _get_team_members(
        self,
        db: AsyncSession,
        project_id: str
    ) -> List[str]:
        """Get team member IDs for a project"""
        query = text("""
            SELECT DISTINCT assignee_id
            FROM tasks
            WHERE project_id = :project_id
              AND assignee_id IS NOT NULL
        """)
        
        result = await db.execute(query, {'project_id': project_id})
        return [row[0] for row in result.fetchall()]
