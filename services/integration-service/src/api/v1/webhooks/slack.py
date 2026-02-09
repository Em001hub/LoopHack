from fastapi import APIRouter, Request
router = APIRouter()

@router.post("/")
async def slack_webhook(request: Request):
    payload = await request.json()
    return {"status": "received"}
