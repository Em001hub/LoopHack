from fastapi import APIRouter
router = APIRouter()

@router.post("/trigger")
def trigger_sync():
    return {"status": "sync started"}
