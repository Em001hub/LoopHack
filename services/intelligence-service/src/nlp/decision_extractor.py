"""
Decision Extractor
Extracts decisions made from conversation text
"""

import re
from typing import List, Dict, Optional
from loguru import logger
from datetime import datetime


class DecisionExtractor:
    """
    Extract decisions from engineering team conversations
    
    **Identifies:**
    - What was decided
    - Who made the decision
    - When it was decided
    - Rationale (if mentioned)
    """
    
    def __init__(self):
        # Decision indicator keywords
        self.decision_indicators = [
            # Definitive decisions
            r'\b(we (?:will|shall|are going to|decided to|agreed to))\b',
            r'\b(let\'s|lets)\b',
            r'\b(going with|choosing|selected|picking)\b',
            
            # Conclusion indicators
            r'\b(final decision|conclusion|resolved)\b',
            r'\b(that settles it|that\'s settled)\b',
            
            # Action commitments
            r'\b(will implement|will use|will go with)\b',
            r'\b(approved|confirmed)\b',
        ]
        
        # Compile regex patterns
        self.decision_patterns = [
            re.compile(pattern, re.IGNORECASE) 
            for pattern in self.decision_indicators
        ]
        
        # Negation patterns (filter out non-decisions)
        self.negation_patterns = [
            re.compile(r'\b(should we|could we|what if|maybe|perhaps|possibly)\b', re.IGNORECASE),
            re.compile(r'\b(not sure|unsure|uncertain|debating)\b', re.IGNORECASE),
            re.compile(r'\?\s*$')  # Ends with question mark
        ]
    
    def extract_decisions(
        self,
        messages: List[Dict],
        min_confidence: float = 0.6
    ) -> List[Dict]:
        """
        Extract all decisions from conversation
        
        **Parameters:**
        messages: List of message dicts with 'user', 'text', 'timestamp'
        min_confidence: Minimum confidence threshold (0-1)
        
        **Returns:**
        List of decisions with metadata
        """
        logger.info(f"🔍 Extracting decisions from {len(messages)} messages")
        
        decisions = []
        
        for msg in messages:
            text = msg.get('text', '')
            if not text:
                continue
            
            # Check if message contains decision
            decision_info = self._analyze_message_for_decision(text)
            
            if decision_info and decision_info['confidence'] >= min_confidence:
                decisions.append({
                    'decision': decision_info['decision_text'],
                    'decided_by': msg.get('user', msg.get('user_email', 'Unknown')),
                    'timestamp': msg.get('timestamp'),
                    'confidence': decision_info['confidence'],
                    'type': decision_info['type'],
                    'rationale': decision_info.get('rationale'),
                    'original_message': text
                })
        
        logger.success(f"✅ Found {len(decisions)} decisions")
        
        return decisions
    
    def _analyze_message_for_decision(self, text: str) -> Optional[Dict]:
        """Analyze single message for decision content"""
        
        # Check for negations first (these are NOT decisions)
        for negation_pattern in self.negation_patterns:
            if negation_pattern.search(text):
                return None
        
        # Check for decision indicators
        matched_pattern = None
        for pattern in self.decision_patterns:
            if pattern.search(text):
                matched_pattern = pattern
                break
        
        if not matched_pattern:
            return None
        
        # Extract the actual decision
        decision_text = self._extract_decision_text(text, matched_pattern)
        
        # Determine decision type
        decision_type = self._classify_decision_type(text)
        
        # Calculate confidence
        confidence = self._calculate_decision_confidence(text, matched_pattern)
        
        # Try to extract rationale
        rationale = self._extract_rationale(text)
        
        return {
            'decision_text': decision_text,
            'confidence': confidence,
            'type': decision_type,
            'rationale': rationale
        }
    
    def _extract_decision_text(self, text: str, pattern: re.Pattern) -> str:
        """Extract the actual decision from message"""
        # Find the match
        match = pattern.search(text)
        if not match:
            return text
        
        # Get text after the decision indicator
        start_pos = match.end()
        decision_text = text[start_pos:].strip()
        
        # Clean up
        # Remove trailing punctuation except period
        decision_text = re.sub(r'[!?;,]+$', '', decision_text)
        
        # Take first sentence if multiple
        sentences = re.split(r'[.!?]\s+', decision_text)
        decision_text = sentences[0] if sentences else decision_text
        
        # Add back the decision indicator for context
        indicator = match.group(0)
        decision_text = f"{indicator} {decision_text}"
        
        return decision_text.strip()
    
    def _classify_decision_type(self, text: str) -> str:
        """Classify the type of decision"""
        text_lower = text.lower()
        
        # Technical decisions
        if any(word in text_lower for word in ['implement', 'use', 'framework', 'library', 'database', 'api', 'architecture']):
            return 'technical'
        
        # Process decisions
        if any(word in text_lower for word in ['process', 'workflow', 'meeting', 'schedule', 'standup']):
            return 'process'
        
        # Resource decisions
        if any(word in text_lower for word in ['hire', 'assign', 'budget', 'resource']):
            return 'resource'
        
        # Timeline decisions
        if any(word in text_lower for word in ['deadline', 'timeline', 'release', 'ship', 'launch']):
            return 'timeline'
        
        # Scope decisions
        if any(word in text_lower for word in ['feature', 'scope', 'requirement', 'cut', 'add']):
            return 'scope'
        
        return 'general'
    
    def _calculate_decision_confidence(self, text: str, pattern: re.Pattern) -> float:
        """Calculate confidence that this is actually a decision"""
        confidence = 0.5  # Base confidence
        
        # Strong indicators increase confidence
        if re.search(r'\b(decided|agreed|final|confirmed)\b', text, re.IGNORECASE):
            confidence += 0.3
        
        # Definitive language
        if re.search(r'\b(will|shall|must)\b', text, re.IGNORECASE):
            confidence += 0.1
        
        # Multiple people agreeing
        if re.search(r'\b(we all|everyone|team)\b', text, re.IGNORECASE):
            confidence += 0.1
        
        # Question marks reduce confidence
        if '?' in text:
            confidence -= 0.2
        
        # Hedging language reduces confidence
        if re.search(r'\b(might|maybe|perhaps|possibly)\b', text, re.IGNORECASE):
            confidence -= 0.3
        
        return max(0.0, min(1.0, confidence))
    
    def _extract_rationale(self, text: str) -> Optional[str]:
        """Try to extract reasoning behind decision"""
        # Look for "because", "since", "as", etc.
        rationale_patterns = [
            r'because\s+(.+?)(?:[.!?]|$)',
            r'since\s+(.+?)(?:[.!?]|$)',
            r'as\s+(.+?)(?:[.!?]|$)',
            r'so that\s+(.+?)(?:[.!?]|$)',
            r'reason:\s*(.+?)(?:[.!?]|$)',
        ]
        
        for pattern in rationale_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                rationale = match.group(1).strip()
                # Don't return if it's too short
                if len(rationale) > 10:
                    return rationale
        
        return None
    
    def group_related_decisions(
        self,
        decisions: List[Dict],
        time_window_minutes: int = 30
    ) -> List[List[Dict]]:
        """
        Group decisions that are related (made close in time)
        
        **Use case:** Multiple decisions in same meeting/discussion
        """
        if not decisions:
            return []
        
        # Sort by timestamp
        sorted_decisions = sorted(
            decisions,
            key=lambda d: datetime.fromisoformat(d['timestamp']) if d.get('timestamp') else datetime.min
        )
        
        groups = []
        current_group = [sorted_decisions[0]]
        
        for decision in sorted_decisions[1:]:
            try:
                current_time = datetime.fromisoformat(decision['timestamp'])
                last_time = datetime.fromisoformat(current_group[-1]['timestamp'])
                
                time_diff = (current_time - last_time).total_seconds() / 60
                
                if time_diff <= time_window_minutes:
                    current_group.append(decision)
                else:
                    groups.append(current_group)
                    current_group = [decision]
            except:
                # If timestamp parsing fails, start new group
                groups.append(current_group)
                current_group = [decision]
        
        # Add last group
        if current_group:
            groups.append(current_group)
        
        logger.info(f"📊 Grouped {len(decisions)} decisions into {len(groups)} discussion threads")
        
        return groups
    
    def summarize_decisions(self, decisions: List[Dict]) -> str:
        """
        Create human-readable summary of decisions
        
        **Returns:**
        Markdown formatted summary
        """
        if not decisions:
            return "No decisions found."
        
        # Group by type
        by_type = {}
        for decision in decisions:
            decision_type = decision.get('type', 'general')
            if decision_type not in by_type:
                by_type[decision_type] = []
            by_type[decision_type].append(decision)
        
        # Build summary
        summary_parts = [f"## Decisions Summary ({len(decisions)} total)\n"]
        
        for decision_type, type_decisions in sorted(by_type.items()):
            summary_parts.append(f"\n### {decision_type.title()} Decisions ({len(type_decisions)})")
            
            for i, decision in enumerate(type_decisions[:5], 1):  # Top 5 per type
                decided_by = decision.get('decided_by', 'Unknown')
                decision_text = decision.get('decision', 'N/A')
                confidence = decision.get('confidence', 0)
                
                summary_parts.append(
                    f"{i}. **{decision_text}**\n"
                    f"   - Decided by: {decided_by}\n"
                    f"   - Confidence: {confidence:.0%}"
                )
                
                if decision.get('rationale'):
                    summary_parts.append(f"   - Rationale: {decision['rationale']}")
        
        return "\n".join(summary_parts)
