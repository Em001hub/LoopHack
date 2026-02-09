from pydantic import BaseModel

class SlackMessage(BaseModel):
    ts: str
    text: str
