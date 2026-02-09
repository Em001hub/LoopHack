from pydantic import BaseModel

class ProjectSchema(BaseModel):
    id: int
    name: str
