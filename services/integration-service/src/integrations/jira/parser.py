from typing import Dict, Any
from datetime import datetime
from src.models.unified import Project, Task, User

def parse_jira_project(raw: Dict[str, Any]) -> Project:
    return Project(
        id=raw['id'],
        name=raw['name'],
        key=raw['key'],
        description=raw.get('description'),
        source='jira',
        url=raw.get('self'),
        metadata={
            'project_type': raw.get('projectTypeKey'),
            'avatar': raw.get('avatarUrls', {}).get('48x48')
        }
    )

def parse_jira_issue(raw: Dict[str, Any], project_id: str) -> Task:
    fields = raw['fields']
    
    # Handle dates
    created_at = datetime.fromisoformat(fields['created'].replace('Z', '+00:00'))
    updated_at = datetime.fromisoformat(fields['updated'].replace('Z', '+00:00'))
    
    completed_at = None
    resolution_date = fields.get('resolutiondate')
    if resolution_date:
        completed_at = datetime.fromisoformat(resolution_date.replace('Z', '+00:00'))

    # Assignee
    assignee_id = None
    if fields.get('assignee'):
        assignee_id = fields['assignee']['accountId']

    # Creator
    creator_id = None
    if fields.get('creator'):
        creator_id = fields['creator']['accountId']

    return Task(
        id=raw['key'],
        project_id=project_id,
        title=fields['summary'],
        description=fields.get('description'),
        status=fields['status']['name'],
        priority=fields.get('priority', {}).get('name'),
        assignee_id=assignee_id,
        creator_id=creator_id,
        created_at=created_at,
        updated_at=updated_at,
        completed_at=completed_at,
        story_points=fields.get('customfield_10016'),  # Common story point field, might vary
        source='jira',
        url=raw['self'],
        labels=fields.get('labels', []),
        metadata={
            'issue_type': fields['issuetype']['name'],
            'raw_status': fields['status']['name'],
            'resolution': fields.get('resolution', {}).get('name') if fields.get('resolution') else None
        }
    )

def parse_jira_user(raw: Dict[str, Any]) -> User:
    return User(
        id=raw['accountId'],
        email=raw.get('emailAddress', ''),
        name=raw.get('displayName'),
        source='jira',
        metadata={
            'avatar': raw.get('avatarUrls', {}).get('48x48'),
            'active': raw.get('active', True)
        }
    )
