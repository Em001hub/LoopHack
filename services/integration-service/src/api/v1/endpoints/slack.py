from fastapi import APIRouter, HTTPException
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
