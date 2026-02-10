from fastapi import APIRouter, Request
router = APIRouter()

@router.post("/")
async def github_webhook(request: Request):
    payload = await request.json()
    return {"status": "received"}
