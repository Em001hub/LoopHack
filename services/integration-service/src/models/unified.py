from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class User(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    source: str  # e.g., 'jira', 'github', 'slack'
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Project(BaseModel):
    id: str
    name: str
    key: Optional[str] = None
    description: Optional[str] = None
    source: str
    url: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Task(BaseModel):
    id: str
    project_id: str
    title: str
    description: Optional[str] = None
    status: str
    priority: Optional[str] = None
    assignee_id: Optional[str] = None
    creator_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    story_points: Optional[float] = None
    source: str
    url: Optional[str] = None
    labels: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Event(BaseModel):
    id: str
    event_type: str  # e.g., 'code_commit', 'issue_update', 'message'
    user_id: str
    project_id: Optional[str] = None
    timestamp: datetime
    source: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
