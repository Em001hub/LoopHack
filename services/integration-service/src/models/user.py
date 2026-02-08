from sqlalchemy import Column, String, DateTime, JSON
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
