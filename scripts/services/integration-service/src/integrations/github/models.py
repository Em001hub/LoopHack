from pydantic import BaseModel

class GitHubPR(BaseModel):
    id: int
    title: str
