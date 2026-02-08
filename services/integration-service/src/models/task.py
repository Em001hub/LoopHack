from sqlalchemy import Column, String, DateTime, Float, JSON, ForeignKey
from src.config.database import Base
from datetime import datetime

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
