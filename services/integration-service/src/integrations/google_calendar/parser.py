from typing import Dict, Any
from datetime import datetime
from src.models.unified import Event

def parse_calendar_event(raw: Dict[str, Any]) -> Event:
    start = raw.get('start', {})
    # Handle both dateTime and date (all-day events)
    start_str = start.get('dateTime') or start.get('date')
    
    if 'T' in start_str:
        timestamp = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
    else:
        timestamp = datetime.fromisoformat(start_str)

    return Event(
        id=raw['id'],
        event_type='meeting',
        user_id=raw.get('creator', {}).get('email', 'unknown'),
        project_id=None,  # Calendar events aren't always tied to a project
        timestamp=timestamp,
        source='google_calendar',
        metadata={
            'summary': raw.get('summary', ''),
            'description': raw.get('description', ''),
            'status': raw.get('status'),
            'location': raw.get('location'),
            'attendees_count': len(raw.get('attendees', [])),
            'html_link': raw.get('htmlLink')
        }
    )
