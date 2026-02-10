"""
Skill Extraction Model
Automatically identifies user skills from code commits, messages, and activity
"""

import numpy as np
import pandas as pd
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from loguru import logger
import re

try:
    import spacy
    SPACY_AVAILABLE = True
except Exception as e:
    SPACY_AVAILABLE = False
    logger.warning(f"spaCy not available: {e}. Using fallback skill extraction.")

from sklearn.feature_extraction.text import TfidfVectorizer


class SkillExtractor:
    """
    ML model for extracting skills from user activity
    
    **Data Sources:**
    - GitHub commits (languages, frameworks, file types)
    - Slack messages (technical topics mentioned)
    - Jira tasks (labeled areas)
    - Code reviews (expertise demonstrated)
    """
    
    def __init__(self):
        # Load spaCy for NLP
        if SPACY_AVAILABLE:
            try:
                self.nlp = spacy.load("en_core_web_sm")
                logger.success("✅ spaCy model loaded")
            except OSError:
                logger.warning("⚠️  spaCy model not found, using fallback")
                self.nlp = None
        else:
            self.nlp = None
        
        # Known technical terms
        self.tech_vocabulary = self._load_tech_vocabulary()
        
        # TF-IDF vectorizer for text analysis
        self.tfidf = TfidfVectorizer(
            max_features=500,
            stop_words='english',
            ngram_range=(1, 2)
        )
    
    def _load_tech_vocabulary(self) -> Dict[str, List[str]]:
        """
        Load comprehensive technical vocabulary
        Maps categories to known terms
        """
        return {
            'languages': [
                'python', 'javascript', 'typescript', 'java', 'c++', 'c#', 'go', 'rust',
                'ruby', 'php', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql',
                'html', 'css', 'bash', 'shell', 'powershell'
            ],
            'frameworks': [
                'react', 'vue', 'angular', 'svelte', 'nextjs', 'nuxt',
                'django', 'flask', 'fastapi', 'express', 'nestjs', 'spring',
                'rails', 'laravel', 'dotnet', '.net',
                'pytorch', 'tensorflow', 'keras', 'scikit-learn'
            ],
            'databases': [
                'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch',
                'cassandra', 'dynamodb', 'sqlite', 'mariadb', 'oracle',
                'sql server', 'neo4j', 'couchdb'
            ],
            'cloud': [
                'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'digitalocean',
                'kubernetes', 'docker', 'terraform', 'ansible', 'jenkins'
            ],
            'domains': [
                'machine learning', 'data science', 'devops', 'frontend', 'backend',
                'full-stack', 'mobile', 'security', 'networking', 'embedded',
                'api design', 'microservices', 'authentication', 'testing'
            ],
            'tools': [
                'git', 'github', 'gitlab', 'bitbucket', 'jira', 'confluence',
                'slack', 'vscode', 'intellij', 'vim', 'emacs', 'postman',
                'figma', 'sketch', 'photoshop'
            ]
        }
    
    def extract_skills_from_github(
        self,
        user_id: str,
        github_events: List[Dict],
        days: int = 90
    ) -> Dict:
        """
        Extract skills from GitHub activity
        
        **Analysis:**
        1. Language usage (from file extensions and commit content)
        2. Framework detection (from imports, dependencies)
        3. Technical areas (from file paths and commit messages)
        4. Code complexity (lines changed, files touched)
        """
        logger.info(f"📊 Extracting skills from {len(github_events)} GitHub events")
        
        # Initialize skill scores
        language_scores = defaultdict(float)
        framework_scores = defaultdict(float)
        area_scores = defaultdict(float)
        
        # Recency weight (more recent = higher weight)
        now = datetime.now()
        
        for event in github_events:
            event_date = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
            days_ago = (now - event_date).days
            
            # Decay weight based on age
            recency_weight = np.exp(-days_ago / 30)  # Half-life of 30 days
            
            # Extract languages from files
            if 'languages' in event.get('metadata', {}):
                for lang, lines in event['metadata']['languages'].items():
                    language_scores[lang.lower()] += lines * recency_weight
            
            # Extract technical areas
            if 'technical_areas' in event.get('metadata', {}):
                for area in event['metadata']['technical_areas']:
                    area_scores[area] += recency_weight * 10
            
            # Analyze commit message for frameworks/tools
            if 'message' in event.get('metadata', {}):
                message = event['metadata']['message'].lower()
                
                for framework in self.tech_vocabulary['frameworks']:
                    if framework in message:
                        framework_scores[framework] += recency_weight * 5
        
        # Normalize scores to 0-1 range
        def normalize_scores(scores: Dict) -> Dict:
            if not scores:
                return {}
            max_score = max(scores.values())
            return {k: round(v / max_score, 2) for k, v in scores.items()}
        
        normalized_languages = normalize_scores(language_scores)
        normalized_frameworks = normalize_scores(framework_scores)
        normalized_areas = normalize_scores(area_scores)
        
        # Calculate overall proficiency levels
        def get_proficiency_level(score: float) -> str:
            if score >= 0.8:
                return "Expert"
            elif score >= 0.6:
                return "Advanced"
            elif score >= 0.4:
                return "Intermediate"
            elif score >= 0.2:
                return "Beginner"
            else:
                return "Novice"
        
        # Build skill profile
        skills = {
            'languages': [
                {
                    'name': lang,
                    'proficiency': score,
                    'level': get_proficiency_level(score),
                    'evidence': f"{int(language_scores[lang])} lines in {days} days"
                }
                for lang, score in sorted(normalized_languages.items(), key=lambda x: x[1], reverse=True)
                if score >= 0.2  # Only include if meaningful usage
            ],
            'frameworks': [
                {
                    'name': fw,
                    'proficiency': score,
                    'level': get_proficiency_level(score),
                    'evidence': f"Used in {int(framework_scores[fw] / 5)} commits"
                }
                for fw, score in sorted(normalized_frameworks.items(), key=lambda x: x[1], reverse=True)
                if score >= 0.2
            ],
            'technical_areas': [
                {
                    'area': area,
                    'proficiency': score,
                    'level': get_proficiency_level(score)
                }
                for area, score in sorted(normalized_areas.items(), key=lambda x: x[1], reverse=True)
                if score >= 0.2
            ]
        }
        
        logger.success(f"✅ Extracted {len(skills['languages'])} languages, {len(skills['frameworks'])} frameworks")
        
        return skills
    
    def extract_skills_from_slack(
        self,
        user_id: str,
        slack_messages: List[Dict]
    ) -> Dict:
        """
        Extract expertise from Slack conversations
        
        **Signals:**
        - Answering technical questions (expertise indicator)
        - Asking questions (learning indicator)
        - Technical terms used
        - Help provided to others
        """
        logger.info(f"💬 Analyzing {len(slack_messages)} Slack messages")
        
        expertise_signals = defaultdict(int)
        learning_signals = defaultdict(int)
        
        for msg in slack_messages:
            text = msg.get('metadata', {}).get('text', '').lower()
            intent = msg.get('metadata', {}).get('intent', '')
            
            # Detect technical terms
            detected_terms = self._detect_technical_terms(text)
            
            if intent == 'help_offer' or 'you can' in text or 'try this' in text:
                # User is helping others - expertise signal
                for term in detected_terms:
                    expertise_signals[term] += 2
            elif intent == 'question' or '?' in text:
                # User is asking - learning signal
                for term in detected_terms:
                    learning_signals[term] += 1
            else:
                # General mention
                for term in detected_terms:
                    expertise_signals[term] += 0.5
        
        # Build expertise profile
        expertise = []
        for term, score in sorted(expertise_signals.items(), key=lambda x: x[1], reverse=True)[:10]:
            learning_score = learning_signals.get(term, 0)
            
            # High help, low questions = expert
            # High questions, low help = learning
            expertise_ratio = score / (learning_score + 1)
            
            if expertise_ratio > 2:
                level = "Expert (helps others frequently)"
            elif expertise_ratio > 1:
                level = "Proficient (active discussions)"
            else:
                level = "Learning (asks questions)"
            
            expertise.append({
                'topic': term,
                'help_count': int(score),
                'question_count': learning_score,
                'level': level
            })
        
        return {'slack_expertise': expertise}
    
    def _detect_technical_terms(self, text: str) -> List[str]:
        """Detect technical terms in text"""
        text_lower = text.lower()
        detected = []
        
        for category, terms in self.tech_vocabulary.items():
            for term in terms:
                if term in text_lower:
                    detected.append(term)
        
        return detected
    
    def combine_skill_profiles(
        self,
        github_skills: Dict,
        slack_skills: Dict,
        jira_skills: Optional[Dict] = None
    ) -> Dict:
        """
        Combine skills from multiple sources into unified profile
        
        **Logic:**
        - GitHub shows actual coding skills
        - Slack shows communication/expertise
        - Jira shows domain areas
        """
        logger.info("🔗 Combining skill profiles from multiple sources")
        
        combined = {
            'technical_skills': github_skills.get('languages', []) + github_skills.get('frameworks', []),
            'domain_expertise': github_skills.get('technical_areas', []),
            'communication_expertise': slack_skills.get('slack_expertise', []),
            'overall_level': self._calculate_overall_level(github_skills),
            'confidence': self._calculate_confidence(github_skills, slack_skills),
            'metadata': {
                'last_updated': datetime.now().isoformat(),
                'sources': ['github', 'slack'] + (['jira'] if jira_skills else [])
            }
        }
        
        logger.success("✅ Skill profile combined")
        
        return combined
    
    def _calculate_overall_level(self, github_skills: Dict) -> str:
        """Calculate overall engineering level"""
        languages = github_skills.get('languages', [])
        
        if not languages:
            return "Junior"
        
        # Count expert/advanced skills
        expert_count = sum(1 for skill in languages if skill['proficiency'] >= 0.8)
        advanced_count = sum(1 for skill in languages if skill['proficiency'] >= 0.6)
        
        if expert_count >= 2 and advanced_count >= 4:
            return "Senior/Staff"
        elif expert_count >= 1 or advanced_count >= 3:
            return "Mid-Level/Senior"
        elif advanced_count >= 1:
            return "Mid-Level"
        else:
            return "Junior"
    
    def _calculate_confidence(self, github_skills: Dict, slack_skills: Dict) -> float:
        """Calculate confidence in skill assessment"""
        github_data_points = len(github_skills.get('languages', [])) + len(github_skills.get('frameworks', []))
        slack_data_points = len(slack_skills.get('slack_expertise', []))
        
        total_data = github_data_points + slack_data_points
        
        # More data = higher confidence
        if total_data >= 20:
            return 0.95
        elif total_data >= 10:
            return 0.85
        elif total_data >= 5:
            return 0.70
        else:
            return 0.50
    
    def recommend_task_match(
        self,
        user_skills: Dict,
        task_requirements: Dict
    ) -> Dict:
        """
        Match user skills to task requirements
        
        **Returns:**
        - Match score (0-1)
        - Matching skills
        - Missing skills
        - Recommendation
        """
        logger.info("🎯 Calculating task-skill match")
        
        required_skills = task_requirements.get('required_skills', [])
        preferred_skills = task_requirements.get('preferred_skills', [])
        
        user_skill_names = [s['name'].lower() for s in user_skills.get('technical_skills', [])]
        
        # Calculate match scores
        required_matches = [skill for skill in required_skills if skill.lower() in user_skill_names]
        preferred_matches = [skill for skill in preferred_skills if skill.lower() in user_skill_names]
        
        # Scoring
        required_score = len(required_matches) / len(required_skills) if required_skills else 1.0
        preferred_score = len(preferred_matches) / len(preferred_skills) if preferred_skills else 1.0
        
        # Weighted overall score
        overall_score = (required_score * 0.7) + (preferred_score * 0.3)
        
        # Recommendation
        if overall_score >= 0.85:
            recommendation = "Excellent match - assign immediately"
        elif overall_score >= 0.65:
            recommendation = "Good match - suitable for this task"
        elif overall_score >= 0.45:
            recommendation = "Partial match - may need support"
        else:
            recommendation = "Poor match - consider other team members"
        
        result = {
            'match_score': round(overall_score, 2),
            'required_skills_matched': required_matches,
            'required_skills_missing': [s for s in required_skills if s.lower() not in user_skill_names],
            'preferred_skills_matched': preferred_matches,
            'recommendation': recommendation,
            'confidence': user_skills.get('confidence', 0.5)
        }
        
        logger.info(f"✅ Match score: {result['match_score']:.0%}")
        
        return result
