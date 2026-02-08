from sqlalchemy import Column, String, DateTime, JSON
from src.config.database import Base
from datetime import datetime

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
