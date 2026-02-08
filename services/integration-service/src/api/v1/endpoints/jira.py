from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Any
from src.integrations.jira.client import JiraClient
from src.integrations.jira.parser import parse_jira_project, parse_jira_issue
from src.models.unified import Project, Task
import os

router = APIRouter()

# In a real app, these would come from a database based on the authenticated organization
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

@router.get("/projects", response_model=List[Project])
async def get_jira_projects():
    if not all([JIRA_DOMAIN, JIRA_EMAIL, JIRA_API_TOKEN]):
        raise HTTPException(status_code=400, detail="Jira credentials not configured")
    
    client = JiraClient(JIRA_DOMAIN, JIRA_EMAIL, JIRA_API_TOKEN)
    try:
        raw_projects = await client.get_projects()
        return [parse_jira_project(p) for p in raw_projects]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/projects/{project_key}/tasks", response_model=List[Task])
async def get_jira_tasks(project_key: str):
    if not all([JIRA_DOMAIN, JIRA_EMAIL, JIRA_API_TOKEN]):
        raise HTTPException(status_code=400, detail="Jira credentials not configured")
    
    client = JiraClient(JIRA_DOMAIN, JIRA_EMAIL, JIRA_API_TOKEN)
    try:
        # We need the project ID for the internal mapping
        raw_projects = await client.get_projects()
        project = next((p for p in raw_projects if p['key'] == project_key), None)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        raw_issues = await client.get_issues(project_key)
        return [parse_jira_issue(i, project['id']) for i in raw_issues]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sync")
async def sync_jira(background_tasks: BackgroundTasks):
    """Trigger a full Jira sync in the background."""
    if not all([JIRA_DOMAIN, JIRA_EMAIL, JIRA_API_TOKEN]):
        raise HTTPException(status_code=400, detail="Jira credentials not configured")
    
    from src.config.database import SessionLocal
    from src.services.sync_service import SyncService
    
    def run_sync():
        db = SessionLocal()
        try:
            sync_service = SyncService(db)
            import asyncio
            asyncio.run(sync_service.sync_jira())
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    background_tasks.add_task(run_sync)
    return {"message": "Jira sync triggered", "status": "processing"}


@router.post("/webhook")
async def jira_webhook(request: Dict[str, Any]):
    """
    Handle Jira webhook events.
    
    Jira sends webhooks for various events like:
    - issue_created
    - issue_updated
    - issue_deleted
    - sprint_started
    - etc.
    """
    # In production, validate webhook signature here
    # from src.integrations.jira.webhook_validator import validate_jira_signature
    # signature = request.headers.get("X-Jira-Signature")
    # if not validate_jira_signature(await request.body(), signature, WEBHOOK_SECRET):
    #     raise HTTPException(status_code=401, detail="Invalid webhook signature")
    
    webhook_event = request.get("webhookEvent")
    
    if not webhook_event:
        raise HTTPException(status_code=400, detail="Missing webhookEvent")
    
    # Process different event types
    if webhook_event == "jira:issue_created":
        issue = request.get("issue", {})
        # Process new issue
        return {"message": "Issue created event processed", "issue_key": issue.get("key")}
    
    elif webhook_event == "jira:issue_updated":
        issue = request.get("issue", {})
        # Process updated issue
        return {"message": "Issue updated event processed", "issue_key": issue.get("key")}
    
    elif webhook_event == "jira:issue_deleted":
        issue = request.get("issue", {})
        # Process deleted issue
        return {"message": "Issue deleted event processed", "issue_key": issue.get("key")}
    
    else:
        # Log unhandled event type
        return {"message": f"Webhook event received: {webhook_event}", "status": "acknowledged"}

