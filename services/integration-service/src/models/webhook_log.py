from sqlalchemy import Column, Integer, String, JSON
from src.config.database import Base

class WebhookLog(Base):
    __tablename__ = "webhook_logs"
    id = Column(Integer, primary_key=True, index=True)
    payload = Column(JSON)
