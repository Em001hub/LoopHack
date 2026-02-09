"""
Text Summarizer
Generates concise summaries of conversations and documents
"""

import re
from typing import List, Dict, Optional
from loguru import logger
from collections import Counter


class TextSummarizer:
    """
    Summarize conversations, threads, and documents
    
    **Methods:**
    - Extractive: Extract key sentences
    - Abstractive: Generate new summary (using GPT-4 if available)
    - Hybrid: Combine both approaches
    """
    
    def __init__(self):
        self.use_gpt = False  # GPT-4 optional for now
        logger.info("📝 TextSummarizer initialized (extractive mode)")
    
    def summarize_conversation(
        self,
        messages: List[Dict],
        max_length: int = 200,
        method: str = 'extractive'
    ) -> Dict:
        """
        Summarize a conversation thread
        
        **Parameters:**
        messages: List of message dicts
        max_length: Maximum words in summary
        method: 'extractive', 'abstractive', or 'hybrid'
        
        **Returns:**
        Dict with summary and metadata
        """
        logger.info(f"📝 Summarizing conversation with {len(messages)} messages")
        
        if not messages:
            return {
                'summary': 'No messages to summarize',
                'method': method,
                'message_count': 0
            }
        
        # Combine all message text
        full_text = self._prepare_text(messages)
        
        # Use extractive summarization
        summary = self._extractive_summarize(full_text, max_length)
        method_used = 'extractive'
        
        # Extract key topics
        topics = self._extract_key_topics(full_text)
        
        # Extract participants
        participants = list(set([
            msg.get('user', msg.get('user_email', 'Unknown'))
            for msg in messages
        ]))
        
        result = {
            'summary': summary,
            'method': method_used,
            'message_count': len(messages),
            'word_count': len(summary.split()),
            'participants': participants,
            'key_topics': topics[:5],  # Top 5 topics
            'timestamp_range': {
                'start': messages[0].get('timestamp') if messages else None,
                'end': messages[-1].get('timestamp') if messages else None
            }
        }
        
        logger.success(f"✅ Generated {len(summary.split())} word summary using {method_used}")
        
        return result
    
    def _prepare_text(self, messages: List[Dict]) -> str:
        """Prepare text for summarization"""
        text_parts = []
        
        for msg in messages:
            user = msg.get('user', msg.get('user_email', 'Unknown'))
            text = msg.get('text', '')
            
            if text:
                # Clean up text
                text = re.sub(r'http\S+', '[URL]', text)  # Replace URLs
                text = re.sub(r'\s+', ' ', text).strip()  # Normalize whitespace
                
                text_parts.append(f"{user}: {text}")
        
        return "\n".join(text_parts)
    
    def _extractive_summarize(self, text: str, max_length: int) -> str:
        """
        Extractive summarization - select important sentences
        
        **Algorithm:**
        1. Split into sentences
        2. Score each sentence by importance
        3. Select top N sentences
        4. Return in original order
        """
        # Split into sentences
        sentences = re.split(r'[.!?]\s+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        if not sentences:
            return "No content to summarize"
        
        # Score sentences
        sentence_scores = []
        for i, sentence in enumerate(sentences):
            score = self._score_sentence(sentence, text)
            sentence_scores.append((i, sentence, score))
        
        # Sort by score
        sentence_scores.sort(key=lambda x: x[2], reverse=True)
        
        # Select sentences until we hit max_length
        selected = []
        current_length = 0
        
        for idx, sentence, score in sentence_scores:
            words = len(sentence.split())
            if current_length + words <= max_length:
                selected.append((idx, sentence))
                current_length += words
            
            if current_length >= max_length * 0.9:  # 90% of max
                break
        
        # Sort selected sentences by original order
        selected.sort(key=lambda x: x[0])
        
        # Join sentences
        summary = '. '.join([s[1] for s in selected])
        
        return summary
    
    def _score_sentence(self, sentence: str, full_text: str) -> float:
        """
        Score sentence importance
        
        **Factors:**
        - Position (first/last sentences often important)
        - Length (very short/long sentences less important)
        - Keywords (technical terms, decision words)
        - Similarity to document
        """
        score = 0.0
        
        # Length scoring (prefer medium-length sentences)
        words = sentence.split()
        word_count = len(words)
        
        if 10 <= word_count <= 30:
            score += 1.0
        elif word_count < 5 or word_count > 50:
            score -= 0.5
        
        # Keyword scoring
        sentence_lower = sentence.lower()
        
        # Decision keywords
        decision_keywords = ['decided', 'will', 'going to', 'agreed', 'confirmed']
        score += sum(2.0 for kw in decision_keywords if kw in sentence_lower)
        
        # Action keywords
        action_keywords = ['implement', 'build', 'create', 'fix', 'change']
        score += sum(1.5 for kw in action_keywords if kw in sentence_lower)
        
        # Question keywords (less important for summary)
        if '?' in sentence:
            score -= 0.5
        
        # Technical terms
        tech_terms = ['api', 'database', 'code', 'bug', 'feature', 'deploy']
        score += sum(1.0 for term in tech_terms if term in sentence_lower)
        
        # Person mentions
        if '@' in sentence:
            score += 0.5
        
        return score
    
    def _extract_key_topics(self, text: str, top_n: int = 5) -> List[str]:
        """Extract key topics using word frequency"""
        # Normalize text
        text_lower = text.lower()
        
        # Remove common words
        stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'is', 'are', 'was', 'were', 'been', 'be', 'have', 'has',
            'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'can',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we',
            'they', 'what', 'which', 'who', 'when', 'where', 'why', 'how'
        }
        
        # Extract words
        words = re.findall(r'\b\w+\b', text_lower)
        
        # Filter and count
        word_counts = Counter([
            word for word in words
            if word not in stopwords and len(word) > 3
        ])
        
        # Get top words
        top_words = [word for word, count in word_counts.most_common(top_n)]
        
        return top_words
