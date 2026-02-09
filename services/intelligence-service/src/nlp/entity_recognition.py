"""
Entity Recognition
Extract named entities from conversations (people, tasks, projects, technologies)
"""

import re
from typing import List, Dict, Set, Optional
from loguru import logger
from collections import Counter

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    logger.warning("spaCy not installed, NER will be limited to pattern-based extraction")


class EntityRecognizer:
    """
    Extract and recognize entities in engineering conversations
    
    **Entity Types:**
    - People (team members, @mentions)
    - Tasks/Issues (Jira IDs, ticket references)
    - Projects (project names)
    - Technologies (languages, frameworks, tools)
    - Repositories (GitHub repos)
    """
    
    def __init__(self):
        # Load spaCy model
        self.nlp = None
        if SPACY_AVAILABLE:
            try:
                self.nlp = spacy.load("en_core_web_sm")
                logger.info("✅ spaCy model loaded")
            except OSError:
                logger.warning("spaCy model not found, NER will be limited")
        
        # Regex patterns for common entities
        self.patterns = {
            'jira_ticket': re.compile(r'\b([A-Z]{2,10}-\d+)\b'),
            'github_pr': re.compile(r'\b(PR[#\s-]*\d+|pull request[#\s-]*\d+)\b', re.IGNORECASE),
            'github_issue': re.compile(r'\b(issue[#\s-]*\d+|#\d+)\b', re.IGNORECASE),
            'mention': re.compile(r'@([\w\-\.]+)'),
            'email': re.compile(r'\b[\w\.-]+@[\w\.-]+\.\w+\b'),
            'url': re.compile(r'https?://[^\s]+'),
            'commit_hash': re.compile(r'\b[0-9a-f]{7,40}\b'),
        }
        
        # Known technology terms
        self.tech_vocabulary = self._load_tech_vocabulary()
    
    def _load_tech_vocabulary(self) -> Dict[str, Set[str]]:
        """Load comprehensive tech vocabulary"""
        return {
            'languages': {
                'python', 'javascript', 'typescript', 'java', 'c++', 'c#', 'go',
                'rust', 'ruby', 'php', 'swift', 'kotlin', 'scala', 'sql', 'r',
                'html', 'css', 'bash', 'shell'
            },
            'frameworks': {
                'react', 'vue', 'angular', 'svelte', 'nextjs', 'django', 'flask',
                'fastapi', 'express', 'spring', 'rails', 'laravel', 'dotnet',
                'pytorch', 'tensorflow', 'keras'
            },
            'databases': {
                'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch',
                'cassandra', 'dynamodb', 'sqlite', 'mariadb'
            },
            'cloud': {
                'aws', 'azure', 'gcp', 'heroku', 'kubernetes', 'docker',
                'terraform', 'ansible'
            },
            'tools': {
                'git', 'github', 'gitlab', 'jira', 'slack', 'vscode',
                'postman', 'figma'
            }
        }
    
    def extract_entities(
        self,
        text: str,
        entity_types: Optional[List[str]] = None
    ) -> Dict[str, List[Dict]]:
        """
        Extract all entities from text
        
        **Parameters:**
        text: Input text
        entity_types: Specific types to extract (None = all)
        
        **Returns:**
        Dict mapping entity type to list of entities
        """
        entities = {
            'people': [],
            'tasks': [],
            'projects': [],
            'technologies': [],
            'repositories': [],
            'urls': [],
            'emails': []
        }
        
        # Extract pattern-based entities
        entities['tasks'].extend(self._extract_task_references(text))
        entities['people'].extend(self._extract_mentions(text))
        entities['emails'].extend(self._extract_emails(text))
        entities['urls'].extend(self._extract_urls(text))
        entities['technologies'].extend(self._extract_technologies(text))
        
        # Use spaCy for person names if available
        if self.nlp:
            spacy_entities = self._extract_with_spacy(text)
            entities['people'].extend(spacy_entities.get('PERSON', []))
            entities['projects'].extend(spacy_entities.get('ORG', []))
        
        # Deduplicate
        for entity_type in entities:
            entities[entity_type] = self._deduplicate_entities(entities[entity_type])
        
        # Filter by requested types
        if entity_types:
            entities = {
                k: v for k, v in entities.items()
                if k in entity_types
            }
        
        return entities
    
    def _extract_task_references(self, text: str) -> List[Dict]:
        """Extract Jira tickets, GitHub issues, PRs"""
        tasks = []
        
        # Jira tickets (e.g., PROJ-123)
        for match in self.patterns['jira_ticket'].finditer(text):
            tasks.append({
                'text': match.group(0),
                'type': 'jira_ticket',
                'start': match.start(),
                'end': match.end()
            })
        
        # GitHub PRs
        for match in self.patterns['github_pr'].finditer(text):
            tasks.append({
                'text': match.group(0),
                'type': 'github_pr',
                'start': match.start(),
                'end': match.end()
            })
        
        # GitHub issues
        for match in self.patterns['github_issue'].finditer(text):
            tasks.append({
                'text': match.group(0),
                'type': 'github_issue',
                'start': match.start(),
                'end': match.end()
            })
        
        return tasks
    
    def _extract_mentions(self, text: str) -> List[Dict]:
        """Extract @mentions"""
        mentions = []
        
        for match in self.patterns['mention'].finditer(text):
            mentions.append({
                'text': match.group(1),
                'type': 'mention',
                'start': match.start(),
                'end': match.end()
            })
        
        return mentions
    
    def _extract_emails(self, text: str) -> List[Dict]:
        """Extract email addresses"""
        emails = []
        
        for match in self.patterns['email'].finditer(text):
            emails.append({
                'text': match.group(0),
                'type': 'email',
                'start': match.start(),
                'end': match.end()
            })
        
        return emails
    
    def _extract_urls(self, text: str) -> List[Dict]:
        """Extract URLs"""
        urls = []
        
        for match in self.patterns['url'].finditer(text):
            url_text = match.group(0)
            
            # Determine URL type
            if 'github.com' in url_text:
                url_type = 'github'
            elif 'jira' in url_text or 'atlassian' in url_text:
                url_type = 'jira'
            elif 'docs.google' in url_text:
                url_type = 'google_docs'
            elif 'figma.com' in url_text:
                url_type = 'figma'
            else:
                url_type = 'general'
            
            urls.append({
                'text': url_text,
                'type': url_type,
                'start': match.start(),
                'end': match.end()
            })
        
        return urls
    
    def _extract_technologies(self, text: str) -> List[Dict]:
        """Extract technology mentions"""
        text_lower = text.lower()
        technologies = []
        
        for category, terms in self.tech_vocabulary.items():
            for term in terms:
                # Find all occurrences
                start = 0
                while True:
                    pos = text_lower.find(term, start)
                    if pos == -1:
                        break
                    
                    # Check if it's a word boundary
                    if pos > 0 and text_lower[pos-1].isalnum():
                        start = pos + 1
                        continue
                    if pos + len(term) < len(text_lower) and text_lower[pos + len(term)].isalnum():
                        start = pos + 1
                        continue
                    
                    technologies.append({
                        'text': text[pos:pos+len(term)],  # Preserve original case
                        'type': 'technology',
                        'category': category,
                        'start': pos,
                        'end': pos + len(term)
                    })
                    
                    start = pos + len(term)
        
        return technologies
    
    def _extract_with_spacy(self, text: str) -> Dict[str, List[Dict]]:
        """Extract entities using spaCy NER"""
        if not self.nlp:
            return {}
        
        doc = self.nlp(text)
        entities_by_type = {}
        
        for ent in doc.ents:
            if ent.label_ not in entities_by_type:
                entities_by_type[ent.label_] = []
            
            entities_by_type[ent.label_].append({
                'text': ent.text,
                'type': ent.label_.lower(),
                'start': ent.start_char,
                'end': ent.end_char
            })
        
        return entities_by_type
    
    def _deduplicate_entities(self, entities: List[Dict]) -> List[Dict]:
        """Remove duplicate entities"""
        seen = set()
        unique = []
        
        for entity in entities:
            # Create key from text and type
            key = (entity['text'].lower(), entity.get('type', 'unknown'))
            
            if key not in seen:
                seen.add(key)
                unique.append(entity)
        
        return unique
    
    def extract_relationships(
        self,
        messages: List[Dict]
    ) -> Dict[str, List[Dict]]:
        """
        Extract relationships between entities
        
        **Examples:**
        - Person X mentioned Task Y
        - Technology Z discussed in context of Project P
        - Person A asked Person B about Task C
        
        **Returns:**
        Dict of relationship types to relationship instances
        """
        relationships = {
            'person_task': [],
            'person_technology': [],
            'task_technology': [],
            'person_person': []
        }
        
        for msg in messages:
            text = msg.get('text', '')
            person = msg.get('user', msg.get('user_email', 'Unknown'))
            
            # Extract entities from this message
            entities = self.extract_entities(text)
            
            # Person → Task relationships
            for task in entities.get('tasks', []):
                relationships['person_task'].append({
                    'person': person,
                    'task': task['text'],
                    'action': 'mentioned',
                    'timestamp': msg.get('timestamp')
                })
            
            # Person → Technology relationships
            for tech in entities.get('technologies', []):
                relationships['person_technology'].append({
                    'person': person,
                    'technology': tech['text'],
                    'category': tech.get('category', 'unknown'),
                    'timestamp': msg.get('timestamp')
                })
            
            # Person → Person relationships (@mentions)
            for mention in entities.get('people', []):
                if mention.get('type') == 'mention':
                    relationships['person_person'].append({
                        'from': person,
                        'to': mention['text'],
                        'action': 'mentioned',
                        'timestamp': msg.get('timestamp')
                    })
        
        logger.info(f"🔗 Extracted {sum(len(v) for v in relationships.values())} relationships")
        
        return relationships
    
    def get_most_mentioned_entities(
        self,
        messages: List[Dict],
        entity_type: str = 'tasks',
        top_n: int = 10
    ) -> List[tuple]:
        """
        Get most frequently mentioned entities
        
        **Returns:**
        List of (entity, count) tuples sorted by count
        """
        entity_counts = Counter()
        
        for msg in messages:
            text = msg.get('text', '')
            entities = self.extract_entities(text, entity_types=[entity_type])
            
            for entity in entities.get(entity_type, []):
                entity_counts[entity['text']] += 1
        
        return entity_counts.most_common(top_n)
    
    def summarize_entities(
        self,
        messages: List[Dict]
    ) -> str:
        """
        Create summary of entities mentioned in conversation
        
        **Returns:**
        Markdown formatted summary
        """
        # Extract all entities
        all_entities = {
            'tasks': Counter(),
            'people': Counter(),
            'technologies': Counter()
        }
        
        for msg in messages:
            text = msg.get('text', '')
            entities = self.extract_entities(text)
            
            for task in entities.get('tasks', []):
                all_entities['tasks'][task['text']] += 1
            
            for person in entities.get('people', []):
                all_entities['people'][person['text']] += 1
            
            for tech in entities.get('technologies', []):
                all_entities['technologies'][tech['text']] += 1
        
        # Build summary
        summary_parts = ["## Entity Summary\n"]
        
        if all_entities['tasks']:
            summary_parts.append(f"### Tasks/Issues ({len(all_entities['tasks'])})")
            for task, count in all_entities['tasks'].most_common(10):
                summary_parts.append(f"- {task} (mentioned {count}x)")
        
        if all_entities['people']:
            summary_parts.append(f"\n### People ({len(all_entities['people'])})")
            for person, count in all_entities['people'].most_common(10):
                summary_parts.append(f"- {person} (mentioned {count}x)")
        
        if all_entities['technologies']:
            summary_parts.append(f"\n### Technologies ({len(all_entities['technologies'])})")
            for tech, count in all_entities['technologies'].most_common(10):
                summary_parts.append(f"- {tech} (mentioned {count}x)")
        
        return "\n".join(summary_parts)
