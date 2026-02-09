from pydantic import BaseModel

class TaskSchema(BaseModel):
    id: int
    title: str
