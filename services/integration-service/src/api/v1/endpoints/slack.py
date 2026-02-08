from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Any
from src.integrations.slack.client import SlackClient
from src.integrations.slack.parser import parse_slack_channel, parse_slack_message, parse_slack_user
from src.models.unified import Project, Event, User
import os

router = APIRouter()

SLACK_TOKEN = os.getenv("SLACK_TOKEN")

@router.get("/channels", response_model=List[Project])
async def get_slack_channels():
    if not SLACK_TOKEN:
        raise HTTPException(status_code=400, detail="Slack token not configured")
    
    client = SlackClient(SLACK_TOKEN)
    try:
        raw_channels = await client.get_channels()
        return [parse_slack_channel(c) for c in raw_channels]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/channels/{channel_id}/messages", response_model=List[Event])
async def get_slack_messages(channel_id: str):
    if not SLACK_TOKEN:
        raise HTTPException(status_code=400, detail="Slack token not configured")
    
    client = SlackClient(SLACK_TOKEN)
    try:
        raw_messages = await client.get_messages(channel_id)
        return [parse_slack_message(m, channel_id) for m in raw_messages]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users", response_model=List[User])
async def get_slack_users():
    if not SLACK_TOKEN:
        raise HTTPException(status_code=400, detail="Slack token not configured")
    
    client = SlackClient(SLACK_TOKEN)
    try:
        raw_users = await client.get_users()
        return [parse_slack_user(u) for u in raw_users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sync")
async def sync_slack(background_tasks: BackgroundTasks):
    """Trigger a full Slack sync in the background."""
    if not SLACK_TOKEN:
        raise HTTPException(status_code=400, detail="Slack token not configured")
    
    from src.config.database import SessionLocal
    from src.services.sync_service import SyncService
    
    def run_sync():
        db = SessionLocal()
        try:
            sync_service = SyncService(db)
            import asyncio
            asyncio.run(sync_service.sync_slack())
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    background_tasks.add_task(run_sync)
    return {"message": "Slack sync triggered", "status": "processing"}


@router.post("/webhook")
async def slack_webhook(request: Dict[str, Any]):
    """
    Handle Slack webhook events.
    
    Slack sends webhooks for events like:
    - message.channels (new message in channel)
    - member_joined_channel
    - app_mention
    - etc.
    """
    # Slack sends a challenge parameter for URL verification
    if "challenge" in request:
        return {"challenge": request["challenge"]}
    
    event_type = request.get("event", {}).get("type")
    
    if event_type == "message":
        # New message event
        event = request.get("event", {})
        return {"message": "Message event processed", "channel": event.get("channel")}
    
    elif event_type == "app_mention":
        # Bot was mentioned
        event = request.get("event", {})
        return {"message": "App mention processed", "user": event.get("user")}
    
    elif event_type == "member_joined_channel":
        # User joined channel
        event = request.get("event", {})
        return {"message": "Member joined event processed", "user": event.get("user")}
    
    else:
        return {"message": f"Webhook event received: {event_type}", "status": "acknowledged"}

