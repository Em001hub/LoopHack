"""Unified sync endpoint to trigger all integrations."""
from fastapi import APIRouter, BackgroundTasks, HTTPException
from typing import Dict, Any
import os
from datetime import datetime

router = APIRouter()


@router.post("/all")
async def sync_all(background_tasks: BackgroundTasks):
    """Trigger sync for all configured integrations."""
    from src.config.database import SessionLocal
    from src.services.sync_service import SyncService
    
    def run_sync():
        db = SessionLocal()
        try:
            sync_service = SyncService(db)
            import asyncio
            asyncio.run(sync_service.sync_all())
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    background_tasks.add_task(run_sync)
    return {
        "message": "Full sync triggered for all integrations",
        "status": "processing",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/status")
async def get_sync_status():
    """Get the status of the last sync operation."""
    # In a production system, this would query a sync_status table
    # For now, return a placeholder
    return {
        "last_sync": None,
        "status": "idle",
        "integrations": {
            "jira": {"enabled": bool(os.getenv("JIRA_DOMAIN")), "last_sync": None},
            "github": {"enabled": bool(os.getenv("GITHUB_TOKEN")), "last_sync": None},
            "slack": {"enabled": bool(os.getenv("SLACK_TOKEN")), "last_sync": None},
            "calendar": {"enabled": bool(os.getenv("GOOGLE_ACCESS_TOKEN")), "last_sync": None}
        }
    }
