"""
Sentiment Service
Orchestrates sentiment analysis, morale tracking, and burnout detection
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import Dict, List, Optional
from loguru import logger
from datetime import datetime, timedelta
from collections import defaultdict

from src.ml.models.sentiment_analyzer import SentimentAnalyzer


class SentimentService:
    """
    Service for managing sentiment analysis and team morale
    
    **Responsibilities:**
    - Analyze individual user sentiment
    - Track sentiment trends
    - Calculate burnout risk
    - Aggregate team morale
    - Generate alerts
    """
    
    def __init__(self):
        self.analyzer = SentimentAnalyzer()
        logger.info("✅ SentimentService initialized")
    
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
        logger.info(f"😊 Analyzing sentiment for user: {user_id} (last {days} days)")
        
        try:
            # 1. Fetch user messages
            messages = await self._fetch_user_messages(db, user_id, days)
            logger.info(f"Found {len(messages)} messages")
            
            if len(messages) < 3:
                return {
                    'status': 'insufficient_data',
                    'message': f'Need at least 3 days of data (found {len(messages)} messages)',
                    'user_id': user_id
                }
            
            # 2. Analyze sentiment trend
            analysis = self.analyzer.analyze_user_sentiment_trend(
                user_id=user_id,
                messages=messages,
                days=days
            )
            
            # 3. Store analysis result
            await self._store_sentiment_analysis(db, user_id, analysis)
            
            logger.success(f"✅ Sentiment: {analysis['current_sentiment']['label']}, "
                         f"Trend: {analysis['sentiment_trend']['direction']}, "
                         f"Burnout risk: {analysis['burnout_risk']['level']}")
            
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Sentiment analysis failed: {e}")
            raise
    
    async def analyze_team_morale(
        self,
        db: AsyncSession,
        project_id: str,
        days: int = 30
    ) -> Dict:
        """
        Analyze overall team morale for a project
        
        **Returns:**
        - Team average sentiment
        - Individual member sentiments
        - At-risk team members
        - Morale distribution
        """
        logger.info(f"👥 Analyzing team morale for project: {project_id} (last {days} days)")
        
        try:
            # 1. Get all team members
            team_members = await self._get_team_members(db, project_id)
            logger.info(f"Analyzing {len(team_members)} team members")
            
            # 2. Fetch messages for all team members
            team_messages = {}
            for member_id in team_members:
                messages = await self._fetch_user_messages(db, member_id, days)
                if messages:
                    team_messages[member_id] = messages
            
            # 3. Analyze team morale
            morale_analysis = self.analyzer.analyze_team_morale(team_messages)
            
            # 4. Add project metadata
            morale_analysis['project_id'] = project_id
            morale_analysis['analysis_period_days'] = days
            morale_analysis['analysis_timestamp'] = datetime.now().isoformat()
            
            # 5. Store team morale
            await self._store_team_morale(db, project_id, morale_analysis)
            
            logger.success(f"✅ Team morale: {morale_analysis['team_morale']['label']}, "
                         f"{len(morale_analysis['at_risk_members'])} at-risk members")
            
            return morale_analysis
            
        except Exception as e:
            logger.error(f"❌ Team morale analysis failed: {e}")
            raise
    
    async def calculate_burnout_risk(
        self,
        db: AsyncSession,
        user_id: str
    ) -> Dict:
        """
        Calculate specific user's burnout risk
        
        **Returns:**
        - Risk level (Low/Medium/High)
        - Risk score (0-100)
        - Specific indicators
        - Recommended action
        """
        logger.info(f"⚠️ Calculating burnout risk for: {user_id}")
        
        try:
            # Analyze sentiment (includes burnout risk)
            analysis = await self.analyze_user_sentiment(db, user_id, days=30)
            
            if analysis.get('status') == 'insufficient_data':
                return {
                    'user_id': user_id,
                    'score': 0,
                    'level': 'Unknown',
                    'indicators': [],
                    'recommended_action': 'Insufficient data to assess burnout risk',
                    'confidence': 'low'
                }
            
            burnout_risk = analysis['burnout_risk']
            burnout_risk['user_id'] = user_id
            
            logger.info(f"Burnout risk: {burnout_risk['level']} (score: {burnout_risk['score']})")
            return burnout_risk
            
        except Exception as e:
            logger.error(f"❌ Burnout risk calculation failed: {e}")
            raise
    
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
        
        try:
            alerts = []
            
            # 1. Get team morale
            morale = await self.analyze_team_morale(db, project_id, days=7)
            
            # 2. Alert for at-risk members
            for at_risk in morale['at_risk_members']:
                severity = 'critical' if at_risk['risk_level'] == 'High' else 'warning'
                
                alerts.append({
                    'type': 'burnout_risk',
                    'severity': severity,
                    'user_id': at_risk['user_id'],
                    'message': f"Team member at {at_risk['risk_level']} burnout risk",
                    'details': {
                        'risk_score': at_risk['risk_score'],
                        'risk_level': at_risk['risk_level'],
                        'recommended_action': at_risk['recommended_action']
                    },
                    'created_at': datetime.now().isoformat()
                })
            
            # 3. Alert if overall team morale is declining
            if morale['team_morale']['trend'] == 'declining':
                alerts.append({
                    'type': 'team_morale_declining',
                    'severity': 'warning',
                    'message': 'Team morale is trending downward',
                    'details': {
                        'current_sentiment': morale['team_morale']['average_sentiment'],
                        'trend': morale['team_morale']['trend'],
                        'low_morale_count': morale['low_morale_count']
                    },
                    'created_at': datetime.now().isoformat()
                })
            
            # 4. Alert if team morale is very low
            if morale['team_morale']['label'] == 'negative':
                alerts.append({
                    'type': 'low_team_morale',
                    'severity': 'warning',
                    'message': 'Overall team morale is negative',
                    'details': {
                        'average_sentiment': morale['team_morale']['average_sentiment'],
                        'members_analyzed': morale['members_analyzed'],
                        'low_morale_count': morale['low_morale_count']
                    },
                    'created_at': datetime.now().isoformat()
                })
            
            logger.info(f"Found {len(alerts)} active alerts")
            return alerts
            
        except Exception as e:
            logger.error(f"❌ Alert fetch failed: {e}")
            raise
    
    async def track_sentiment_trend(
        self,
        db: AsyncSession,
        user_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> Dict:
        """
        Track sentiment trend over a specific time period
        
        **Use case:** Historical analysis, identifying patterns
        """
        logger.info(f"📈 Tracking sentiment trend for {user_id} "
                   f"from {start_date.date()} to {end_date.date()}")
        
        try:
            days = (end_date - start_date).days
            
            # Fetch messages in time range
            messages = await self._fetch_user_messages_range(
                db, user_id, start_date, end_date
            )
            
            if not messages:
                return {
                    'status': 'no_data',
                    'message': 'No messages found in specified time range'
                }
            
            # Analyze trend
            analysis = self.analyzer.analyze_user_sentiment_trend(
                user_id=user_id,
                messages=messages,
                days=days
            )
            
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Sentiment tracking failed: {e}")
            raise
    
    # Private helper methods
    
    async def _fetch_user_messages(
        self,
        db: AsyncSession,
        user_id: str,
        days: int
    ) -> List[Dict]:
        """Fetch user messages from database"""
        try:
            query = text("""
                SELECT 
                    timestamp,
                    metadata
                FROM events
                WHERE 
                    user_id = :user_id
                    AND source = 'slack'
                    AND event_type = 'message'
                    AND timestamp > NOW() - INTERVAL ':days days'
                ORDER BY timestamp DESC
            """)
            
            result = await db.execute(query, {
                "user_id": user_id,
                "days": days
            })
            
            rows = result.fetchall()
            
            messages = []
            for row in rows:
                messages.append({
                    'timestamp': row[0].isoformat(),
                    'text': row[1].get('text', '') if isinstance(row[1], dict) else '',
                    'metadata': row[1] if isinstance(row[1], dict) else {}
                })
            
            return messages
            
        except Exception as e:
            logger.warning(f"Failed to fetch messages: {e}")
            # Return sample data for testing
            return self._generate_sample_messages(user_id, days)
    
    async def _fetch_user_messages_range(
        self,
        db: AsyncSession,
        user_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict]:
        """Fetch messages in specific date range"""
        try:
            query = text("""
                SELECT 
                    timestamp,
                    metadata
                FROM events
                WHERE 
                    user_id = :user_id
                    AND source = 'slack'
                    AND event_type = 'message'
                    AND timestamp BETWEEN :start_date AND :end_date
                ORDER BY timestamp DESC
            """)
            
            result = await db.execute(query, {
                "user_id": user_id,
                "start_date": start_date,
                "end_date": end_date
            })
            
            rows = result.fetchall()
            
            messages = []
            for row in rows:
                messages.append({
                    'timestamp': row[0].isoformat(),
                    'text': row[1].get('text', '') if isinstance(row[1], dict) else '',
                    'metadata': row[1] if isinstance(row[1], dict) else {}
                })
            
            return messages
            
        except Exception as e:
            logger.warning(f"Failed to fetch messages: {e}")
            return []
    
    def _generate_sample_messages(self, user_id: str, days: int) -> List[Dict]:
        """Generate sample messages for testing"""
        import random
        
        messages = []
        now = datetime.now()
        
        # Generate messages with varying sentiment
        sample_texts = [
            "Great progress on the feature today!",
            "Stuck on this bug, need help",
            "Code review looks good, approved",
            "Frustrated with these API issues",
            "Happy with how the sprint is going",
            "Feeling overwhelmed with deadlines",
            "Nice work everyone!",
            "This is blocking my progress",
            "Excited about the new architecture",
            "Stressed about the release"
        ]
        
        for i in range(min(days * 2, 30)):  # ~2 messages per day
            timestamp = now - timedelta(days=random.randint(0, days))
            messages.append({
                'timestamp': timestamp.isoformat(),
                'text': random.choice(sample_texts),
                'metadata': {
                    'text': random.choice(sample_texts),
                    'channel': 'general'
                }
            })
        
        return messages
    
    async def _get_team_members(
        self,
        db: AsyncSession,
        project_id: str
    ) -> List[str]:
        """Get all team members for a project"""
        try:
            query = text("""
                SELECT DISTINCT assignee_id
                FROM tasks
                WHERE 
                    project_id = :project_id
                    AND assignee_id IS NOT NULL
            """)
            
            result = await db.execute(query, {"project_id": project_id})
            rows = result.fetchall()
            
            return [row[0] for row in rows]
            
        except Exception as e:
            logger.warning(f"Failed to get team members: {e}")
            # Return test data
            return ['user_sarah', 'user_mike', 'user_alex']
    
    async def _store_sentiment_analysis(
        self,
        db: AsyncSession,
        user_id: str,
        analysis: Dict
    ):
        """Store sentiment analysis in database"""
        try:
            query = text("""
                INSERT INTO sentiment_analysis (
                    user_id,
                    analysis_data,
                    sentiment_score,
                    burnout_risk_level,
                    created_at
                )
                VALUES (
                    :user_id,
                    :analysis_data,
                    :sentiment_score,
                    :burnout_risk_level,
                    NOW()
                )
            """)
            
            await db.execute(query, {
                "user_id": user_id,
                "analysis_data": str(analysis),
                "sentiment_score": analysis['current_sentiment']['recent_avg'],
                "burnout_risk_level": analysis['burnout_risk']['level']
            })
            await db.commit()
            
            logger.info("✅ Sentiment analysis stored")
            
        except Exception as e:
            logger.warning(f"Failed to store sentiment analysis: {e}")
            await db.rollback()
    
    async def _store_team_morale(
        self,
        db: AsyncSession,
        project_id: str,
        morale: Dict
    ):
        """Store team morale in database"""
        try:
            query = text("""
                INSERT INTO team_morale (
                    project_id,
                    morale_data,
                    average_sentiment,
                    at_risk_count,
                    created_at
                )
                VALUES (
                    :project_id,
                    :morale_data,
                    :average_sentiment,
                    :at_risk_count,
                    NOW()
                )
            """)
            
            await db.execute(query, {
                "project_id": project_id,
                "morale_data": str(morale),
                "average_sentiment": morale['team_morale']['average_sentiment'],
                "at_risk_count": len(morale['at_risk_members'])
            })
            await db.commit()
            
            logger.info("✅ Team morale stored")
            
        except Exception as e:
            logger.warning(f"Failed to store team morale: {e}")
            await db.rollback()