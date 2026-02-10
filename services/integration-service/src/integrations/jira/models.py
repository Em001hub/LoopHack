from pydantic import BaseModel

class JiraIssue(BaseModel):
    id: str
    key: str
    summary: str
