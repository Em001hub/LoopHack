from fastapi import APIRouter, Request
router = APIRouter()

@router.post("/")
async def calendar_webhook(request: Request):
    # Google calendar webhook verification and processing
    return {"status": "received"}
