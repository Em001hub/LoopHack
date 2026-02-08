from typing import Dict, Any, List
from datetime import datetime
from src.models.unified import Project, Event, User

def parse_slack_channel(raw: Dict[str, Any]) -> Project:
    return Project(
        id=raw['id'],
        name=raw['name'],
        key=raw['name'],
        description=raw.get('topic', {}).get('value'),
        source='slack',
        metadata={
            'is_private': raw.get('is_private', False),
            'num_members': raw.get('num_members', 0)
        }
    )

def parse_slack_message(raw: Dict[str, Any], channel_id: str) -> Event:
    # Handle timestamp
    ts = float(raw['ts'])
    timestamp = datetime.fromtimestamp(ts)

    return Event(
        id=raw['ts'],
        event_type='slack_message',
        user_id=raw.get('user', 'unknown'),
        project_id=channel_id,
        timestamp=timestamp,
        source='slack',
        metadata={
            'text': raw.get('text', ''),
            'thread_ts': raw.get('thread_ts'),
            'reply_count': raw.get('reply_count', 0)
        }
    )

def parse_slack_user(raw: Dict[str, Any]) -> User:
    profile = raw.get('profile', {})
    return User(
        id=raw['id'],
        email=profile.get('email', ''),
        name=profile.get('real_name') or raw.get('name'),
        source='slack',
        metadata={
            'avatar': profile.get('image_48'),
            'is_bot': raw.get('is_bot', False),
            'title': profile.get('title')
        }
    )
