"""
Insight Generator Service
Aggregates predictions, sentiment, and skills to generate actionable insights
"""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from loguru import logger

from src.services.prediction_service import PredictionService
from src.services.skill_service import SkillService
from src.services.sentiment_service import SentimentService


class InsightGenerator:
    """
    High-level service that combines all ML models
    to generate actionable business insights
    
    **Use Cases:**
    - Daily project standup insights
    - Weekly executive summaries
    - Task assignment recommendations
    - Risk identification and mitigation
    """
    
    def __init__(self):
        self.prediction_service = PredictionService()
        self.skill_service = SkillService()
        self.sentiment_service = SentimentService()
        logger.info("✅ InsightGenerator initialized")
    
    async def generate_daily_insights(
        self,
        db: AsyncSession,
        project_id: str
    ) -> Dict:
        """
        Generate comprehensive daily insights for a project
        
        **Combines:**
        - Timeline predictions
        - Team morale
        - Blockers and risks
        - Opportunities
        
        **Output:** Structured insights ready for display
        """
        logger.info(f"🔮 Generating daily insights for project: {project_id}")
        
        try:
            # 1. Get timeline prediction
            timeline = await self.prediction_service.predict_project_timeline(
                db=db,
                project_id=project_id
            )
            
            # 2. Get team sentiment
            team_morale = await self.sentiment_service.analyze_team_morale(
                db=db,
                project_id=project_id,
                days=7  # Last week
            )
            
            # 3. Identify risks
            risks = await self._identify_project_risks(
                db=db,
                project_id=project_id,
                timeline=timeline,
                morale=team_morale
            )
            
            # 4. Find opportunities
            opportunities = await self._find_opportunities(
                db=db,
                project_id=project_id
            )
            
            # 5. Generate summary
            summary = self._generate_summary(timeline, team_morale, risks)
            
            # 6. Create highlights
            highlights = self._create_highlights(timeline, team_morale, risks)
            
            insights = {
                'project_id': project_id,
                'date': datetime.now().date().isoformat(),
                'summary': summary,
                'highlights': highlights,
                'timeline': {
                    'predicted_completion': timeline['predicted_completion_date'],
                    'weeks_remaining': timeline['predicted_weeks_remaining'],
                    'probability_on_time': timeline.get('probability_on_time'),
                    'confidence': timeline['model_confidence']
                },
                'team_morale': {
                    'overall': team_morale['team_morale']['label'],
                    'average_score': team_morale['team_morale']['average_sentiment'],
                    'trend': team_morale['team_morale']['trend'],
                    'at_risk_count': len(team_morale['at_risk_members'])
                },
                'risks': risks,
                'opportunities': opportunities,
                'recommended_actions': self._generate_actions(risks, opportunities)
            }
            
            logger.success(f"✅ Generated insights with {len(risks)} risks, {len(opportunities)} opportunities")
            return insights
            
        except Exception as e:
            logger.error(f"❌ Failed to generate insights: {e}")
            raise
    
    async def generate_weekly_summary(
        self,
        db: AsyncSession,
        project_id: str
    ) -> Dict:
        """
        Generate executive-level weekly summary
        
        **Focus:**
        - High-level progress
        - Key risks
        - Major decisions needed
        - Resource recommendations
        """
        logger.info(f"📊 Generating weekly summary for: {project_id}")
        
        try:
            # Get data for the week
            timeline = await self.prediction_service.predict_project_timeline(
                db=db,
                project_id=project_id
            )
            
            team_morale = await self.sentiment_service.analyze_team_morale(
                db=db,
                project_id=project_id,
                days=7
            )
            
            # Calculate progress
            project_data = await self.prediction_service.get_project_data(db, project_id)
            
            summary = {
                'project_id': project_id,
                'week_ending': datetime.now().date().isoformat(),
                'executive_summary': self._create_executive_summary(
                    timeline,
                    team_morale,
                    project_data
                ),
                'key_metrics': {
                    'completion_probability': timeline.get('probability_on_time'),
                    'predicted_completion': timeline['predicted_completion_date'],
                    'team_morale': team_morale['team_morale']['label'],
                    'velocity_trend': 'stable',  # Would calculate from data
                    'blocker_count': project_data.get('blocked_tasks_count', 0)
                },
                'highlights': {
                    'accomplishments': [],  # Would fetch from completed tasks
                    'challenges': self._extract_challenges(timeline, team_morale),
                    'decisions_needed': []  # Would extract from conversations
                },
                'next_week_focus': self._suggest_next_week_focus(timeline, team_morale),
                'resource_recommendations': self._generate_resource_recommendations(
                    project_data,
                    team_morale
                )
            }
            
            logger.success("✅ Weekly summary generated")
            return summary
            
        except Exception as e:
            logger.error(f"❌ Failed to generate weekly summary: {e}")
            raise
    
    async def get_task_recommendations(
        self,
        db: AsyncSession,
        task_id: str
    ) -> Dict:
        """
        Get AI recommendations for a specific task
        
        **Returns:**
        - Best assignee
        - Estimated complexity
        - Similar tasks
        - Potential blockers
        """
        logger.info(f"🎯 Generating recommendations for task: {task_id}")
        
        try:
            # Would fetch task details from database
            # For now, using placeholder logic
            
            recommendations = {
                'task_id': task_id,
                'assignment': {
                    'recommended_assignee': 'sarah@company.com',
                    'match_score': 0.92,
                    'reasoning': 'Strong React skills (0.92 proficiency), available capacity',
                    'alternative_assignees': [
                        {
                            'assignee': 'mike@company.com',
                            'match_score': 0.78,
                            'reasoning': 'Good React skills, currently on similar task'
                        }
                    ]
                },
                'complexity': {
                    'estimated_hours': 6,
                    'confidence': 0.75,
                    'factors': [
                        'Similar to PROJ-120 (8 hours)',
                        'Requires API integration',
                        'UI complexity: medium'
                    ]
                },
                'dependencies': [
                    'PROJ-120 (design mockups) - must complete first',
                    'PROJ-115 (API endpoint) - parallel work possible'
                ],
                'potential_blockers': [
                    'May need design feedback - schedule early review',
                    'API endpoint not yet deployed to staging'
                ],
                'related_tasks': [
                    {'task_id': 'PROJ-130', 'similarity': 0.85, 'title': 'Similar auth work'}
                ]
            }
            
            logger.success("✅ Task recommendations generated")
            return recommendations
            
        except Exception as e:
            logger.error(f"❌ Failed to generate task recommendations: {e}")
            raise
    
    async def _identify_project_risks(
        self,
        db: AsyncSession,
        project_id: str,
        timeline: Dict,
        morale: Dict
    ) -> List[Dict]:
        """Identify all project risks"""
        risks = []
        
        # Timeline risks
        if timeline.get('probability_on_time', 1.0) < 0.7:
            risks.append({
                'type': 'timeline',
                'severity': 'high' if timeline.get('probability_on_time', 0) < 0.5 else 'medium',
                'description': f"Only {timeline.get('probability_on_time', 0):.0%} chance of on-time delivery",
                'recommended_action': 'Consider scope reduction or adding resources',
                'impact': 'May miss deadline'
            })
        
        # Risk factors from prediction
        for risk_factor in timeline.get('risk_factors', []):
            if 'blocked' in risk_factor.lower():
                risks.append({
                    'type': 'blocker',
                    'severity': 'medium',
                    'description': risk_factor,
                    'recommended_action': 'Prioritize unblocking tasks',
                    'impact': 'Slows team velocity'
                })
        
        # Morale risks
        for at_risk in morale.get('at_risk_members', []):
            risks.append({
                'type': 'burnout',
                'severity': at_risk['risk_level'].lower(),
                'description': f"Team member at {at_risk['risk_level']} burnout risk",
                'recommended_action': at_risk['recommended_action'],
                'impact': 'May lose team member or reduced productivity'
            })
        
        return risks
    
    async def _find_opportunities(
        self,
        db: AsyncSession,
        project_id: str
    ) -> List[str]:
        """Find opportunities to improve project"""
        opportunities = []
        
        # Would analyze:
        # - Available capacity
        # - Skill matches
        # - Process improvements
        
        # Placeholder opportunities
        opportunities = [
            'Mike has availability - consider assigning frontend tasks',
            'Code review queue is empty - good time to open new PRs',
            'Velocity is stable - good time to tackle complex features'
        ]
        
        return opportunities
    
    def _generate_summary(
        self,
        timeline: Dict,
        morale: Dict,
        risks: List[Dict]
    ) -> str:
        """Generate natural language summary"""
        
        # Timeline status
        weeks = timeline['predicted_weeks_remaining']
        prob = timeline.get('probability_on_time', 0)
        
        if prob and prob > 0.8:
            timeline_status = f"Project is on track to complete in {weeks:.1f} weeks"
        elif prob and prob > 0.6:
            timeline_status = f"Project has moderate risk, estimated {weeks:.1f} weeks remaining"
        else:
            timeline_status = f"Project is at risk, needs attention"
        
        # Morale status
        morale_label = morale['team_morale']['label']
        at_risk_count = len(morale['at_risk_members'])
        
        if at_risk_count == 0:
            morale_status = "Team morale is good"
        elif at_risk_count == 1:
            morale_status = "One team member showing stress signals"
        else:
            morale_status = f"{at_risk_count} team members showing stress signals"
        
        # Risk status
        high_risks = [r for r in risks if r['severity'] == 'high']
        if high_risks:
            risk_status = f"{len(high_risks)} high-priority risks require attention"
        elif risks:
            risk_status = f"{len(risks)} risks identified"
        else:
            risk_status = "No major risks identified"
        
        return f"{timeline_status}. {morale_status}. {risk_status}."
    
    def _create_highlights(
        self,
        timeline: Dict,
        morale: Dict,
        risks: List[Dict]
    ) -> List[str]:
        """Create bullet point highlights"""
        highlights = []
        
        # Timeline highlight
        if timeline.get('probability_on_time', 0) > 0.8:
            highlights.append(f"✅ On track for completion ({timeline.get('probability_on_time', 0):.0%} confidence)")
        else:
            highlights.append(f"⚠️ Timeline risk ({timeline.get('probability_on_time', 0):.0%} on-time probability)")
        
        # Morale highlight
        if morale['team_morale']['label'] == 'positive':
            highlights.append("✅ Team morale is positive")
        else:
            at_risk = len(morale['at_risk_members'])
            if at_risk > 0:
                highlights.append(f"⚠️ {at_risk} team member(s) at burnout risk")
        
        # Risk highlights
        for risk in risks[:2]:  # Top 2 risks
            emoji = "🔴" if risk['severity'] == 'high' else "⚠️"
            highlights.append(f"{emoji} {risk['description']}")
        
        return highlights
    
    def _generate_actions(
        self,
        risks: List[Dict],
        opportunities: List[str]
    ) -> List[Dict]:
        """Generate recommended actions"""
        actions = []
        
        # Actions for high-priority risks
        high_risks = [r for r in risks if r['severity'] == 'high']
        for risk in high_risks:
            actions.append({
                'priority': 'high',
                'action': risk['recommended_action'],
                'reason': risk['description']
            })
        
        # Actions for medium risks
        medium_risks = [r for r in risks if r['severity'] == 'medium']
        for risk in medium_risks[:2]:  # Top 2 medium risks
            actions.append({
                'priority': 'medium',
                'action': risk['recommended_action'],
                'reason': risk['description']
            })
        
        return actions
    
    def _create_executive_summary(
        self,
        timeline: Dict,
        morale: Dict,
        project_data: Dict
    ) -> str:
        """Create executive summary (2-3 sentences)"""
        
        prob = timeline.get('probability_on_time', 0)
        weeks = timeline['predicted_weeks_remaining']
        
        if prob and prob > 0.8:
            status = "green"
            message = f"Project is healthy and on track to complete in approximately {weeks:.0f} weeks."
        elif prob and prob > 0.6:
            status = "yellow"
            message = f"Project has moderate risk with {weeks:.0f} weeks estimated. Recommend monitoring closely."
        else:
            status = "red"
            message = f"Project is at high risk. Estimated {weeks:.0f} weeks but significant challenges exist."
        
        # Add morale note
        at_risk = len(morale['at_risk_members'])
        if at_risk > 0:
            message += f" Team health needs attention: {at_risk} member(s) showing stress signals."
        
        return message
    
    def _extract_challenges(
        self,
        timeline: Dict,
        morale: Dict
    ) -> List[str]:
        """Extract key challenges"""
        challenges = []
        
        # From timeline risks
        for risk in timeline.get('risk_factors', []):
            challenges.append(risk)
        
        # From morale
        if morale['team_morale']['trend'] == 'declining':
            challenges.append("Team morale trending downward")
        
        return challenges
    
    def _suggest_next_week_focus(
        self,
        timeline: Dict,
        morale: Dict
    ) -> List[str]:
        """Suggest focus areas for next week"""
        focus_areas = []
        
        # Based on risks
        if timeline.get('risk_factors'):
            focus_areas.append("Address blockers to maintain velocity")
        
        if len(morale['at_risk_members']) > 0:
            focus_areas.append("Check in with team members showing stress")
        
        focus_areas.append("Continue current sprint work")
        
        return focus_areas
    
    def _generate_resource_recommendations(
        self,
        project_data: Dict,
        morale: Dict
    ) -> List[str]:
        """Recommend resource changes"""
        recommendations = []
        
        # If velocity is low
        if project_data.get('avg_weekly_velocity', 10) < 5:
            recommendations.append("Consider adding 1-2 developers to increase velocity")
        
        # If team is stressed
        if len(morale['at_risk_members']) > 1:
            recommendations.append("Reduce scope or extend timeline to reduce team stress")
        
        # If blockers are high
        if project_data.get('blocked_tasks_count', 0) > 3:
            recommendations.append("Assign dedicated resource to unblock tasks")
        
        return recommendations
