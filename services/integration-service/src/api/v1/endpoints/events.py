from fastapi import APIRouter
router = APIRouter()

@router.get("/")
def get_events():
    return [{"id": 1, "title": "Meeting"}]
