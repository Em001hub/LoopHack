from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Any
from src.integrations.google_calendar.client import GoogleCalendarClient
from src.integrations.google_calendar.parser import parse_calendar_event
from src.models.unified import Event
import os

router = APIRouter()

GOOGLE_ACCESS_TOKEN = os.getenv("GOOGLE_ACCESS_TOKEN")

@router.get("/events", response_model=List[Event])
async def get_calendar_events(calendar_id: str = "primary"):
    if not GOOGLE_ACCESS_TOKEN:
        raise HTTPException(status_code=400, detail="Google Access Token not configured")
    
    client = GoogleCalendarClient(access_token=GOOGLE_ACCESS_TOKEN)
    try:
        raw_events = await client.get_events(calendar_id)
        return [parse_calendar_event(e) for e in raw_events]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sync")
async def sync_calendar(background_tasks: BackgroundTasks):
    """Trigger a full Google Calendar sync in the background."""
    if not GOOGLE_ACCESS_TOKEN:
        raise HTTPException(status_code=400, detail="Google Access Token not configured")
    
    from src.config.database import SessionLocal
    from src.services.sync_service import SyncService
    
    def run_sync():
        db = SessionLocal()
        try:
            sync_service = SyncService(db)
            import asyncio
            asyncio.run(sync_service.sync_calendar())
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    background_tasks.add_task(run_sync)
    return {"message": "Calendar sync triggered", "status": "processing"}


@router.post("/webhook")
async def calendar_webhook(request: Dict[str, Any]):
    """
    Handle Google Calendar webhook notifications.
    
    Google Calendar sends notifications when:
    - Events are created
    - Events are updated
    - Events are deleted
    """
    # Google Calendar uses channel notifications
    # The X-Goog-Channel-ID and X-Goog-Resource-State headers contain metadata
    
    resource_state = request.get("resourceState", "sync")
    
    if resource_state == "exists":
        # Event was created or updated
        return {"message": "Calendar event updated", "status": "processed"}
    
    elif resource_state == "not_exists":
        # Event was deleted
        return {"message": "Calendar event deleted", "status": "processed"}
    
    elif resource_state == "sync":
        # Initial sync message
        return {"message": "Calendar sync notification", "status": "acknowledged"}
    
    else:
        return {"message": f"Webhook received: {resource_state}", "status": "acknowledged"}

