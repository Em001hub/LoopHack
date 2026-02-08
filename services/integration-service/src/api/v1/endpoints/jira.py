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
    # This would trigger a full background sync
    return {"message": "Sync triggered"}
