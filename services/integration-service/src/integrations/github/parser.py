from typing import Dict, Any, List
from datetime import datetime
from src.models.unified import Project, Task, Event, User

def parse_github_repo(raw: Dict[str, Any]) -> Project:
    return Project(
        id=str(raw['id']),
        name=raw['name'],
        key=raw['full_name'],
        description=raw.get('description'),
        source='github',
        url=raw['html_url'],
        metadata={
            'language': raw.get('language'),
            'stars': raw.get('stargazers_count'),
            'forks': raw.get('forks_count')
        }
    )

def parse_github_commit(raw: Dict[str, Any], project_id: str) -> Event:
    commit_data = raw['commit']
    author = commit_data['author']
    
    # Handle dates
    timestamp = datetime.fromisoformat(author['date'].replace('Z', '+00:00'))

    return Event(
        id=raw['sha'],
        event_type='code_commit',
        user_id=raw.get('author', {}).get('login', author['email']),
        project_id=project_id,
        timestamp=timestamp,
        source='github',
        metadata={
            'message': commit_data['message'],
            'url': raw['html_url']
        }
    )

def parse_github_pr(raw: Dict[str, Any], project_id: str) -> Task:
    # Handle dates
    created_at = datetime.fromisoformat(raw['created_at'].replace('Z', '+00:00'))
    updated_at = datetime.fromisoformat(raw['updated_at'].replace('Z', '+00:00'))
    
    completed_at = None
    if raw.get('merged_at'):
        completed_at = datetime.fromisoformat(raw['merged_at'].replace('Z', '+00:00'))
    elif raw.get('closed_at'):
        completed_at = datetime.fromisoformat(raw['closed_at'].replace('Z', '+00:00'))

    return Task(
        id=str(raw['number']),
        project_id=project_id,
        title=raw['title'],
        description=raw.get('body'),
        status=raw['state'],
        priority=None,
        assignee_id=raw.get('assignee', {}).get('login') if raw.get('assignee') else None,
        creator_id=raw.get('user', {}).get('login'),
        created_at=created_at,
        updated_at=updated_at,
        completed_at=completed_at,
        story_points=None,
        source='github',
        url=raw['html_url'],
        labels=[label['name'] for label in raw.get('labels', [])],
        metadata={
            'is_merged': raw.get('merged_at') is not None,
            'base_branch': raw.get('base', {}).get('ref'),
            'head_branch': raw.get('head', {}).get('ref')
        }
    )
