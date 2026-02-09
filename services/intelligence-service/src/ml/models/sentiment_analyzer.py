"""
Sentiment Analysis Model
Analyzes team morale and detects burnout risk from communications
"""

import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from loguru import logger
from collections import defaultdict

try:
    from transformers import pipeline
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logger.warning("Transformers not available, using fallback sentiment analysis")


class SentimentAnalyzer:
    """
    NLP model for analyzing sentiment in team communications
    
    **Use Cases:**
    - Team morale tracking
    - Burnout risk detection
    - Frustration identification
    - Positive engagement measurement
    """
    
    def __init__(self):
        logger.info("Loading sentiment analysis model...")
        
        # Load pre-trained sentiment model
        if TRANSFORMERS_AVAILABLE:
            try:
                self.sentiment_pipeline = pipeline(
                    "sentiment-analysis",
                    model="distilbert-base-uncased-finetuned-sst-2-english",
                    device=0 if torch.cuda.is_available() else -1
                )
                self.use_ml = True
                logger.success("✅ Sentiment model loaded (ML)")
            except Exception as e:
                logger.warning(f"Failed to load ML model: {e}, using fallback")
                self.use_ml = False
        else:
            self.use_ml = False
            logger.info("Using keyword-based sentiment analysis")
        
        # Emotional keywords for fine-grained analysis
        self.emotion_keywords = {
            'frustration': ['frustrated', 'stuck', 'blocked', 'annoying', 'difficult', 'issue', 'problem'],
            'stress': ['overwhelmed', 'stressed', 'pressure', 'urgent', 'deadline', 'behind'],
            'confidence': ['confident', 'sure', 'easy', 'simple', 'straightforward', 'clear'],
            'uncertainty': ['unsure', 'confused', 'unclear', 'not sure', "don't know", 'maybe'],
            'positive': ['great', 'awesome', 'excellent', 'good', 'perfect', 'love', 'happy'],
            'negative': ['bad', 'terrible', 'awful', 'hate', 'worst', 'horrible']
        }
    
    def analyze_message(self, text: str) -> Dict:
        """
        Analyze sentiment of a single message
        
        **Returns:**
        - score: -1 (negative) to +1 (positive)
        - label: 'positive', 'negative', or 'neutral'
        - emotions: Detected emotional signals
        - confidence: Model confidence
        """
        try:
            if self.use_ml:
                # Get base sentiment from ML model
                result = self.sentiment_pipeline(text[:512])[0]  # Limit to 512 tokens
                
                # Convert to numeric score
                if result['label'] == 'POSITIVE':
                    base_score = result['score']
                else:
                    base_score = -result['score']
                
                confidence = result['score']
            else:
                # Fallback: keyword-based sentiment
                base_score, confidence = self._keyword_sentiment(text)
            
            # Detect specific emotions
            emotions = self._detect_emotions(text)
            
            # Adjust score based on emotions
            adjusted_score = base_score
            if 'frustration' in emotions or 'stress' in emotions:
                adjusted_score -= 0.2
            if 'positive' in emotions:
                adjusted_score += 0.1
            
            # Clamp to [-1, 1]
            adjusted_score = max(-1, min(1, adjusted_score))
            
            # Determine label
            if adjusted_score > 0.3:
                label = 'positive'
            elif adjusted_score < -0.3:
                label = 'negative'
            else:
                label = 'neutral'
            
            return {
                'score': round(adjusted_score, 2),
                'label': label,
                'emotions': emotions,
                'confidence': confidence
            }
            
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return {
                'score': 0,
                'label': 'neutral',
                'emotions': [],
                'confidence': 0
            }
    
    def _keyword_sentiment(self, text: str) -> tuple:
        """Fallback keyword-based sentiment analysis"""
        text_lower = text.lower()
        
        positive_count = sum(1 for word in self.emotion_keywords['positive'] if word in text_lower)
        negative_count = sum(1 for word in self.emotion_keywords['negative'] if word in text_lower)
        
        total = positive_count + negative_count
        if total == 0:
            return 0.0, 0.5
        
        score = (positive_count - negative_count) / total
        confidence = min(total / 5.0, 1.0)  # More keywords = higher confidence
        
        return score, confidence
    
    def _detect_emotions(self, text: str) -> List[str]:
        """Detect emotional keywords in text"""
        text_lower = text.lower()
        detected = []
        
        for emotion, keywords in self.emotion_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected.append(emotion)
        
        return detected
    
    def analyze_user_sentiment_trend(
        self,
        user_id: str,
        messages: List[Dict],
        days: int = 30
    ) -> Dict:
        """
        Analyze sentiment trend for a user over time
        
        **Detects:**
        - Overall morale direction (improving/declining)
        - Burnout risk signals
        - Emotional patterns
        """
        logger.info(f"📊 Analyzing sentiment trend for user {user_id}")
        
        # Group messages by day
        daily_sentiments = defaultdict(list)
        
        for msg in messages:
            timestamp = datetime.fromisoformat(msg['timestamp'].replace('Z', '+00:00'))
            day = timestamp.date()
            
            # Analyze message
            sentiment = self.analyze_message(msg.get('text', ''))
            daily_sentiments[day].append(sentiment['score'])
        
        # Calculate daily averages
        daily_avg = {
            day: np.mean(scores)
            for day, scores in daily_sentiments.items()
        }
        
        # Sort by date
        sorted_days = sorted(daily_avg.keys())
        scores = [daily_avg[day] for day in sorted_days]
        
        if len(scores) < 3:
            return {
                'status': 'insufficient_data',
                'message': 'Need at least 3 days of data'
            }
        
        # Calculate trend (linear regression slope)
        x = np.arange(len(scores))
        trend_slope = np.polyfit(x, scores, 1)[0]
        
        # Recent sentiment (last 7 days)
        recent_scores = scores[-7:] if len(scores) >= 7 else scores
        recent_avg = np.mean(recent_scores)
        
        # Overall sentiment (all time)
        overall_avg = np.mean(scores)
        
        # Detect burnout risk
        burnout_risk = self._calculate_burnout_risk({
            'sentiment_trend': trend_slope,
            'recent_sentiment': recent_avg,
            'overall_sentiment': overall_avg,
            'messages': messages
        })
        
        result = {
            'user_id': user_id,
            'period_days': days,
            'sentiment_trend': {
                'direction': 'improving' if trend_slope > 0.01 else 'declining' if trend_slope < -0.01 else 'stable',
                'slope': round(trend_slope, 3),
                'change_per_week': round(trend_slope * 7, 2)
            },
            'current_sentiment': {
                'recent_avg': round(recent_avg, 2),
                'overall_avg': round(overall_avg, 2),
                'label': self._score_to_label(recent_avg)
            },
            'burnout_risk': burnout_risk,
            'daily_scores': [
                {
                    'date': str(day),
                    'score': round(daily_avg[day], 2)
                }
                for day in sorted_days
            ]
        }
        
        logger.success(f"✅ Trend: {result['sentiment_trend']['direction']}, Risk: {burnout_risk['level']}")
        
        return result
    
    def _score_to_label(self, score: float) -> str:
        """Convert numeric score to label"""
        if score > 0.3:
            return 'positive'
        elif score < -0.3:
            return 'negative'
        else:
            return 'neutral'
    
    def _calculate_burnout_risk(self, data: Dict) -> Dict:
        """
        Calculate burnout risk score
        
        **Indicators:**
        - Declining sentiment trend
        - Consistently negative sentiment
        - Frustration/stress keywords
        - High message volume (especially after hours)
        """
        risk_score = 0
        indicators = []
        
        # 1. Declining sentiment (30 points)
        if data['sentiment_trend'] < -0.02:
            risk_score += 30
            indicators.append("Sentiment declining over time")
        
        # 2. Low recent sentiment (25 points)
        if data['recent_sentiment'] < -0.3:
            risk_score += 25
            indicators.append("Recent sentiment consistently negative")
        
        # 3. Frustration signals (20 points)
        frustration_count = sum(
            1 for msg in data['messages']
            if 'frustration' in self._detect_emotions(msg.get('text', ''))
        )
        if frustration_count > len(data['messages']) * 0.2:  # >20% frustrated
            risk_score += 20
            indicators.append(f"High frustration signals ({frustration_count} messages)")
        
        # 4. Stress signals (15 points)
        stress_count = sum(
            1 for msg in data['messages']
            if 'stress' in self._detect_emotions(msg.get('text', ''))
        )
        if stress_count > len(data['messages']) * 0.15:  # >15% stressed
            risk_score += 15
            indicators.append(f"Stress signals detected ({stress_count} messages)")
        
        # 5. Overall negative sentiment (10 points)
        if data['overall_sentiment'] < -0.2:
            risk_score += 10
            indicators.append("Overall sentiment negative")
        
        # Determine risk level
        if risk_score >= 60:
            level = "High"
            action = "Immediate manager intervention recommended"
        elif risk_score >= 35:
            level = "Medium"
            action = "Schedule 1-on-1 to check in"
        else:
            level = "Low"
            action = "No immediate action needed"
        
        return {
            'score': risk_score,
            'level': level,
            'indicators': indicators,
            'recommended_action': action
        }
    
    def analyze_team_morale(
        self,
        team_messages: Dict[str, List[Dict]]
    ) -> Dict:
        """
        Analyze overall team morale
        
        **Input:**
        team_messages: Dict of user_id -> list of messages
        
        **Returns:**
        - Team average sentiment
        - Individual member sentiments
        - At-risk team members
        - Team morale trend
        """
        logger.info(f"👥 Analyzing morale for team of {len(team_messages)} members")
        
        member_sentiments = {}
        at_risk_members = []
        
        for user_id, messages in team_messages.items():
            if not messages:
                continue
            
            # Analyze individual
            user_analysis = self.analyze_user_sentiment_trend(user_id, messages)
            
            if user_analysis.get('status') != 'insufficient_data':
                member_sentiments[user_id] = user_analysis
                
                # Check burnout risk
                if user_analysis['burnout_risk']['level'] in ['Medium', 'High']:
                    at_risk_members.append({
                        'user_id': user_id,
                        'risk_level': user_analysis['burnout_risk']['level'],
                        'risk_score': user_analysis['burnout_risk']['score'],
                        'recommended_action': user_analysis['burnout_risk']['recommended_action']
                    })
        
        # Calculate team averages
        if member_sentiments:
            team_avg = np.mean([
                m['current_sentiment']['recent_avg']
                for m in member_sentiments.values()
            ])
            
            team_trend = np.mean([
                m['sentiment_trend']['slope']
                for m in member_sentiments.values()
            ])
        else:
            team_avg = 0
            team_trend = 0
        
        result = {
            'team_morale': {
                'average_sentiment': round(team_avg, 2),
                'label': self._score_to_label(team_avg),
                'trend': 'improving' if team_trend > 0.01 else 'declining' if team_trend < -0.01 else 'stable'
            },
            'members_analyzed': len(member_sentiments),
            'at_risk_members': at_risk_members,
            'high_morale_count': sum(1 for m in member_sentiments.values() if m['current_sentiment']['recent_avg'] > 0.3),
            'low_morale_count': sum(1 for m in member_sentiments.values() if m['current_sentiment']['recent_avg'] < -0.3),
            'member_details': member_sentiments
        }
        
        logger.success(f"✅ Team morale: {result['team_morale']['label']}, {len(at_risk_members)} at-risk")
        
        return result
