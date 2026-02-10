from sqlalchemy import Column, Integer, String
from src.config.database import Base

class Integration(Base):
    __tablename__ = "integrations"
    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String)
