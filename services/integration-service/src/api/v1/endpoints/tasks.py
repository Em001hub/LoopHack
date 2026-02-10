from fastapi import APIRouter
router = APIRouter()

@router.get("/")
def get_tasks():
    return [{"id": 1, "title": "Task 1"}]
