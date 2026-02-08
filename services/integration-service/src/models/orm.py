from sqlalchemy import Column, String, DateTime, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database import Base
from datetime import datetime

class UserORM(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    email = Column(String, index=True)
    name = Column(String)
    source = Column(String)
    metadata_json = Column(JSON, default={})
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ProjectORM(Base):
    __tablename__ = "projects"
    id = Column(String, primary_key=True)
    name = Column(String)
    key = Column(String, index=True)
    description = Column(String)
    source = Column(String)
    url = Column(String)
    metadata_json = Column(JSON, default={})
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TaskORM(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True)
    project_id = Column(String, ForeignKey("projects.id"))
    title = Column(String)
    description = Column(String)
    status = Column(String)
    priority = Column(String)
    assignee_id = Column(String, ForeignKey("users.id"), nullable=True)
    creator_id = Column(String, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    completed_at = Column(DateTime, nullable=True)
    story_points = Column(Float, nullable=True)
    source = Column(String)
    url = Column(String)
    labels = Column(JSON, default=[])
    metadata_json = Column(JSON, default={})

class EventORM(Base):
    __tablename__ = "events"
    id = Column(String, primary_key=True)
    event_type = Column(String)
    user_id = Column(String, ForeignKey("users.id"))
    project_id = Column(String, ForeignKey("projects.id"), nullable=True)
    timestamp = Column(DateTime)
    source = Column(String)
    metadata_json = Column(JSON, default={})
