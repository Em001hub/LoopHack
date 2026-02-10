"""
Conversation Intelligence using GPT-4
Extracts decisions, action items, and blockers from Slack threads
"""

import json
from typing import Dict, List, Optional
from loguru import logger
from datetime import datetime

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI not available, using fallback conversation parsing")

from src.config.settings import settings


class ConversationParser:
    """
    Advanced NLP for understanding engineering conversations
    
    **Uses GPT-4 to:**
    - Extract key decisions made
    - Identify action items and owners
    - Detect blockers mentioned
    - Summarize discussions
    - Auto-create follow-up tasks
    """
    
    def __init__(self):
        if not OPENAI_AVAILABLE:
            logger.warning("⚠️  OpenAI library not installed")
            self.enabled = False
        elif not settings.OPENAI_API_KEY:
            logger.warning("⚠️  OpenAI API key not configured")
            self.enabled = False
        else:
            openai.api_key = settings.OPENAI_API_KEY
            self.enabled = True
            logger.info("✅ OpenAI client initialized")
        
        self.model = settings.OPENAI_MODEL
    
    def parse_conversation_thread(
        self,
        messages: List[Dict],
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Parse a conversation thread to extract intelligence
        
        **Input:**
        messages: List of messages with user, text, timestamp
        context: Optional context (project, task IDs, etc.)
        
        **Returns:**
        - topic: Main discussion topic
        - decisions: List of decisions made
        - action_items: List of tasks with owners
        - blockers: List of blockers mentioned
        - summary: Natural language summary
        """
        if not self.enabled:
            logger.warning("Conversation parsing disabled (no API key)")
            return self._fallback_parsing(messages)
        
        logger.info(f"🤖 Parsing conversation with {len(messages)} messages")
        
        try:
            # Format conversation for GPT-4
            conversation_text = self._format_conversation(messages)
            
            # Create prompt
            prompt = self._create_parsing_prompt(conversation_text, context)
            
            # Call GPT-4
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at analyzing engineering team conversations. Extract key information accurately and concisely."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.3,  # Lower temperature for more consistent output
                max_tokens=1000
            )
            
            # Parse response
            result = json.loads(response.choices[0].message.content)
            
            # Add metadata
            result['metadata'] = {
                'parsed_at': datetime.now().isoformat(),
                'message_count': len(messages),
                'model': self.model,
                'confidence': 'high' if len(messages) >= 3 else 'medium'
            }
            
            logger.success(f"✅ Parsed: {len(result.get('decisions', []))} decisions, {len(result.get('action_items', []))} actions")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Conversation parsing failed: {e}")
            return self._fallback_parsing(messages)
    
    def _format_conversation(self, messages: List[Dict]) -> str:
        """Format messages into readable conversation"""
        formatted = []
        
        for msg in messages:
            user = msg.get('user_email', msg.get('user_id', 'Unknown'))
            timestamp = msg.get('timestamp', '')
            text = msg.get('text', msg.get('metadata', {}).get('text', ''))
            
            formatted.append(f"[{timestamp}] {user}: {text}")
        
        return "\n".join(formatted)
    
    def _create_parsing_prompt(self, conversation: str, context: Optional[Dict]) -> str:
        """Create GPT-4 prompt for parsing"""
        context_str = ""
        if context:
            context_str = f"\n\nContext: {json.dumps(context, indent=2)}"
        
        return f"""Analyze this engineering team conversation and extract structured information.

Conversation:
{conversation}
{context_str}

Extract the following as JSON:
{{
    "topic": "Main topic or problem being discussed (1 sentence)",
    "summary": "Brief summary of the conversation (2-3 sentences)",
    "decisions": [
        {{
            "decision": "What was decided",
            "rationale": "Why (if mentioned)",
            "decided_by": "Who made the decision (if clear)"
        }}
    ],
    "action_items": [
        {{
            "action": "What needs to be done",
            "owner": "Person responsible (email or name)",
            "deadline": "When it's needed (if mentioned, else null)",
            "priority": "high/medium/low based on urgency indicators"
        }}
    ],
    "blockers": [
        {{
            "blocker": "Description of the blocker",
            "blocked_item": "What is blocked (task ID if mentioned)",
            "waiting_on": "Person or team being waited on",
            "type": "technical/process/external/information"
        }}
    ],
    "questions": [
        {{
            "question": "Unanswered question text",
            "asker": "Who asked"
        }}
    ],
    "is_resolved": true/false,
    "requires_followup": true/false,
    "technical_topics": ["list", "of", "technical", "topics", "mentioned"]
}}

Rules:
- Only include items explicitly mentioned in the conversation
- Use null for unknown values
- Be precise and concise
- Extract emails/names exactly as they appear
"""
    
    def _fallback_parsing(self, messages: List[Dict]) -> Dict:
        """Simple keyword-based parsing when GPT-4 unavailable"""
        logger.info("Using fallback parsing (keyword-based)")
        
        # Simple keyword detection
        text_all = " ".join([m.get('text', '') for m in messages]).lower()
        
        blockers = []
        if any(word in text_all for word in ['blocked', 'waiting', 'stuck']):
            blockers.append({
                'blocker': 'Blocker mentioned (see conversation)',
                'type': 'unknown'
            })
        
        action_items = []
        if any(word in text_all for word in ['will', 'going to', 'should']):
            action_items.append({
                'action': 'Action item detected (see conversation)',
                'owner': 'unknown'
            })
        
        return {
            'topic': 'Discussion detected',
            'summary': f"Conversation with {len(messages)} messages",
            'decisions': [],
            'action_items': action_items,
            'blockers': blockers,
            'questions': [],
            'is_resolved': False,
            'requires_followup': len(blockers) > 0 or len(action_items) > 0,
            'metadata': {
                'parsing_method': 'fallback',
                'confidence': 'low'
            }
        }
    
    def generate_summary(self, conversation_analysis: Dict) -> str:
        """
        Generate human-readable summary
        
        **Returns:**
        Natural language summary suitable for digests/reports
        """
        topic = conversation_analysis.get('topic', 'Discussion')
        decisions = conversation_analysis.get('decisions', [])
        actions = conversation_analysis.get('action_items', [])
        blockers = conversation_analysis.get('blockers', [])
        
        summary_parts = [f"**{topic}**"]
        
        if decisions:
            summary_parts.append(f"\n✅ Decisions: {len(decisions)}")
            for d in decisions[:2]:  # Show first 2
                summary_parts.append(f"  • {d['decision']}")
        
        if actions:
            summary_parts.append(f"\n📋 Action Items: {len(actions)}")
            for a in actions[:2]:
                owner = a.get('owner', 'Unknown')
                summary_parts.append(f"  • {a['action']} ({owner})")
        
        if blockers:
            summary_parts.append(f"\n⚠️  Blockers: {len(blockers)}")
            for b in blockers[:2]:
                summary_parts.append(f"  • {b['blocker']}")
        
        return "\n".join(summary_parts)
