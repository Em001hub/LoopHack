from sqlalchemy import Column, Integer, String, DateTime
from src.config.database import Base

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
