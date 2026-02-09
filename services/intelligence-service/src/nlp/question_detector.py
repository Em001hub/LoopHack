"""
Question Detector
Identifies unanswered questions in team conversations
"""

import re
from typing import List, Dict, Optional, Set
from loguru import logger
from datetime import datetime, timedelta


class QuestionDetector:
    """
    Detect questions in conversations and identify which are unanswered
    
    **Use Cases:**
    - Find blockers (unanswered technical questions)
    - Identify knowledge gaps
    - Alert when questions go unanswered too long
    """
    
    def __init__(self):
        # Question word patterns
        self.question_words = [
            r'\b(what|when|where|who|why|how|which)\b',
            r'\b(can|could|would|should|will|is|are|do|does|did)\b',
            r'\b(any|anyone|anybody)\b'
        ]
        
        # Compile patterns
        self.question_patterns = [
            re.compile(pattern, re.IGNORECASE)
            for pattern in self.question_words
        ]
        
        # Answer indicator patterns
        self.answer_indicators = [
            r'\b(yes|no|yeah|yep|nope)\b',
            r'\b(here\'s|here is|here are)\b',
            r'\b(you can|you should|try)\b',
            r'\b(the answer is|solution is)\b',
            r'\b(@\w+)\s+(here|check|see)',  # Directed response
        ]
        
        self.answer_patterns = [
            re.compile(pattern, re.IGNORECASE)
            for pattern in self.answer_indicators
        ]
    
    def detect_questions(
        self,
        messages: List[Dict],
        min_confidence: float = 0.6
    ) -> List[Dict]:
        """
        Detect all questions in conversation
        
        **Parameters:**
        messages: List of message dicts with 'user', 'text', 'timestamp'
        min_confidence: Minimum confidence threshold (0-1)
        
        **Returns:**
        List of questions with metadata
        """
        logger.info(f"❓ Detecting questions in {len(messages)} messages")
        
        questions = []
        
        for i, msg in enumerate(messages):
            text = msg.get('text', '')
            if not text:
                continue
            
            # Check if this is a question
            question_info = self._analyze_message_for_question(text)
            
            if question_info and question_info['confidence'] >= min_confidence:
                # Check if answered in subsequent messages
                is_answered, answer_info = self._check_if_answered(
                    messages[i:],  # Messages after this one
                    msg
                )
                
                questions.append({
                    'question': question_info['question_text'],
                    'asker': msg.get('user', msg.get('user_email', 'Unknown')),
                    'timestamp': msg.get('timestamp'),
                    'confidence': question_info['confidence'],
                    'type': question_info['type'],
                    'is_answered': is_answered,
                    'answered_by': answer_info.get('answerer') if is_answered else None,
                    'answered_at': answer_info.get('timestamp') if is_answered else None,
                    'answer_text': answer_info.get('answer') if is_answered else None,
                    'urgency': question_info['urgency'],
                    'original_message': text
                })
        
        unanswered_count = sum(1 for q in questions if not q['is_answered'])
        logger.success(f"✅ Found {len(questions)} questions ({unanswered_count} unanswered)")
        
        return questions
    
    def _analyze_message_for_question(self, text: str) -> Optional[Dict]:
        """Analyze if message contains a question"""
        
        # Obvious indicator: ends with '?'
        has_question_mark = text.strip().endswith('?')
        
        # Check for question words
        has_question_word = any(
            pattern.search(text) 
            for pattern in self.question_patterns
        )
        
        # Must have at least one indicator
        if not (has_question_mark or has_question_word):
            return None
        
        # Calculate confidence
        confidence = self._calculate_question_confidence(text, has_question_mark)
        
        # Determine question type
        question_type = self._classify_question_type(text)
        
        # Determine urgency
        urgency = self._determine_urgency(text)
        
        return {
            'question_text': text.strip(),
            'confidence': confidence,
            'type': question_type,
            'urgency': urgency
        }
    
    def _calculate_question_confidence(
        self,
        text: str,
        has_question_mark: bool
    ) -> float:
        """Calculate confidence that this is actually a question"""
        
        confidence = 0.3  # Base
        
        # Question mark is strong signal
        if has_question_mark:
            confidence += 0.5
        
        # Question words
        question_word_count = sum(
            1 for pattern in self.question_patterns
            if pattern.search(text)
        )
        confidence += min(question_word_count * 0.1, 0.3)
        
        # Statements reduce confidence
        if re.search(r'\b(I think|I believe|In my opinion)\b', text, re.IGNORECASE):
            confidence -= 0.2
        
        # Commands reduce confidence
        if text.strip().startswith(('Please', 'Can you', 'Could you')):
            confidence += 0.1  # Actually increases for polite questions
        
        return max(0.0, min(1.0, confidence))
    
    def _classify_question_type(self, text: str) -> str:
        """Classify the type of question"""
        text_lower = text.lower()
        
        # Technical question
        if any(word in text_lower for word in [
            'how do', 'how to', 'error', 'bug', 'code', 'implement',
            'api', 'database', 'function', 'method', 'syntax'
        ]):
            return 'technical'
        
        # Clarification question
        if any(word in text_lower for word in [
            'what do you mean', 'can you clarify', 'not sure',
            'confused', 'understand', 'explain'
        ]):
            return 'clarification'
        
        # Status question
        if any(word in text_lower for word in [
            'when will', 'is it done', 'status', 'eta', 'progress',
            'finished', 'complete'
        ]):
            return 'status'
        
        # Permission/approval question
        if any(word in text_lower for word in [
            'should i', 'can i', 'may i', 'is it ok', 'approve'
        ]):
            return 'permission'
        
        # Information request
        if any(word in text_lower for word in [
            'where is', 'who has', 'what is', 'which'
        ]):
            return 'information'
        
        return 'general'
    
    def _determine_urgency(self, text: str) -> str:
        """Determine urgency level of question"""
        text_lower = text.lower()
        
        # High urgency indicators
        if any(word in text_lower for word in [
            'urgent', 'asap', 'immediately', 'critical', 'blocker',
            'blocked', 'stuck', 'help', 'emergency'
        ]):
            return 'high'
        
        # Medium urgency
        if any(word in text_lower for word in [
            'soon', 'today', 'needed', 'waiting'
        ]):
            return 'medium'
        
        return 'low'
    
    def _check_if_answered(
        self,
        subsequent_messages: List[Dict],
        question_msg: Dict
    ) -> tuple[bool, Dict]:
        """
        Check if question was answered in subsequent messages
        
        **Logic:**
        - Look for answer indicators in next N messages
        - Check for @mentions of the asker
        - Look for direct responses (threading)
        """
        
        asker = question_msg.get('user', question_msg.get('user_email', ''))
        
        # Check next 10 messages (or less if not available)
        check_window = subsequent_messages[1:11]  # Skip the question itself
        
        for msg in check_window:
            text = msg.get('text', '')
            
            # Check for answer indicators
            has_answer_indicator = any(
                pattern.search(text)
                for pattern in self.answer_patterns
            )
            
            # Check if it mentions the asker
            mentions_asker = f"@{asker}" in text or asker in text
            
            # Check if it's in a thread (same thread_ts)
            same_thread = (
                question_msg.get('thread_ts') and
                msg.get('thread_ts') == question_msg.get('thread_ts')
            )
            
            # If it looks like an answer
            if has_answer_indicator or mentions_asker or same_thread:
                return True, {
                    'answerer': msg.get('user', msg.get('user_email', 'Unknown')),
                    'timestamp': msg.get('timestamp'),
                    'answer': text
                }
        
        return False, {}
    
    def find_unanswered_questions(
        self,
        questions: List[Dict],
        max_age_hours: int = 24
    ) -> List[Dict]:
        """
        Filter to only unanswered questions
        
        **Parameters:**
        max_age_hours: Only include questions newer than this
        
        **Returns:**
        Unanswered questions sorted by urgency and age
        """
        now = datetime.now()
        unanswered = []
        
        for q in questions:
            # Skip if answered
            if q.get('is_answered'):
                continue
            
            # Check age
            try:
                question_time = datetime.fromisoformat(q['timestamp'])
                age_hours = (now - question_time).total_seconds() / 3600
                
                if age_hours > max_age_hours:
                    continue
                
                q['age_hours'] = age_hours
                unanswered.append(q)
                
            except:
                # If timestamp parsing fails, include it anyway
                q['age_hours'] = 0
                unanswered.append(q)
        
        # Sort by urgency then age
        urgency_order = {'high': 0, 'medium': 1, 'low': 2}
        unanswered.sort(
            key=lambda q: (
                urgency_order.get(q.get('urgency', 'low'), 2),
                -q.get('age_hours', 0)
            )
        )
        
        logger.info(f"⚠️  Found {len(unanswered)} unanswered questions")
        
        return unanswered
    
    def generate_alerts(
        self,
        unanswered_questions: List[Dict]
    ) -> List[Dict]:
        """
        Generate alerts for unanswered questions
        
        **Returns:**
        List of alerts with recommended actions
        """
        alerts = []
        
        for q in unanswered_questions:
            age_hours = q.get('age_hours', 0)
            urgency = q.get('urgency', 'low')
            question_type = q.get('type', 'general')
            
            # Determine severity
            if urgency == 'high' and age_hours > 2:
                severity = 'critical'
                action = 'Immediate response needed'
            elif urgency == 'high' or age_hours > 12:
                severity = 'high'
                action = 'Response needed soon'
            elif age_hours > 24:
                severity = 'medium'
                action = 'Follow up recommended'
            else:
                severity = 'low'
                action = 'Monitor'
            
            # Skip low severity unless technical blocker
            if severity == 'low' and question_type != 'technical':
                continue
            
            alerts.append({
                'type': 'unanswered_question',
                'severity': severity,
                'question': q['question'],
                'asker': q['asker'],
                'age_hours': age_hours,
                'urgency': urgency,
                'question_type': question_type,
                'recommended_action': action,
                'timestamp': q['timestamp']
            })
        
        logger.info(f"🚨 Generated {len(alerts)} alerts for unanswered questions")
        
        return alerts
    
    def summarize_questions(self, questions: List[Dict]) -> str:
        """
        Create human-readable summary of questions
        
        **Returns:**
        Markdown formatted summary
        """
        if not questions:
            return "No questions detected."
        
        answered = [q for q in questions if q.get('is_answered')]
        unanswered = [q for q in questions if not q.get('is_answered')]
        
        summary_parts = [
            f"## Questions Summary",
            f"- Total: {len(questions)}",
            f"- Answered: {len(answered)}",
            f"- **Unanswered: {len(unanswered)}**\n"
        ]
        
        if unanswered:
            summary_parts.append("### ⚠️  Unanswered Questions")
            
            # Group by urgency
            by_urgency = {'high': [], 'medium': [], 'low': []}
            for q in unanswered:
                by_urgency[q.get('urgency', 'low')].append(q)
            
            for urgency in ['high', 'medium', 'low']:
                if by_urgency[urgency]:
                    summary_parts.append(f"\n**{urgency.title()} Urgency ({len(by_urgency[urgency])})**")
                    
                    for i, q in enumerate(by_urgency[urgency][:5], 1):
                        age_hours = q.get('age_hours', 0)
                        summary_parts.append(
                            f"{i}. {q['question']}\n"
                            f"   - Asked by: {q['asker']}\n"
                            f"   - Age: {age_hours:.1f} hours\n"
                            f"   - Type: {q.get('type', 'general')}"
                        )
        
        return "\n".join(summary_parts)
