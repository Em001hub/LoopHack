from fastapi import APIRouter, HTTPException
from typing import List
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
