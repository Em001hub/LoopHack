from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Any
from src.integrations.github.client import GitHubClient
from src.integrations.github.parser import parse_github_repo, parse_github_commit, parse_github_pr
from src.models.unified import Project, Task, Event
import os

router = APIRouter()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

@router.get("/repositories", response_model=List[Project])
async def get_github_repos():
    if not GITHUB_TOKEN:
        raise HTTPException(status_code=400, detail="GitHub token not configured")
    
    client = GitHubClient(GITHUB_TOKEN)
    try:
        raw_repos = await client.get_repositories()
        return [parse_github_repo(r) for r in raw_repos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/repositories/{owner}/{repo}/commits", response_model=List[Event])
async def get_github_commits(owner: str, repo: str):
    if not GITHUB_TOKEN:
        raise HTTPException(status_code=400, detail="GitHub token not configured")
    
    client = GitHubClient(GITHUB_TOKEN)
    try:
        raw_commits = await client.get_commits(owner, repo)
        return [parse_github_commit(c, f"{owner}/{repo}") for c in raw_commits]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/repositories/{owner}/{repo}/pulls", response_model=List[Task])
async def get_github_pulls(owner: str, repo: str):
    if not GITHUB_TOKEN:
        raise HTTPException(status_code=400, detail="GitHub token not configured")
    
    client = GitHubClient(GITHUB_TOKEN)
    try:
        raw_pulls = await client.get_pull_requests(owner, repo)
        return [parse_github_pr(p, f"{owner}/{repo}") for p in raw_pulls]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sync")
async def sync_github(background_tasks: BackgroundTasks):
    """Trigger a full GitHub sync in the background."""
    if not GITHUB_TOKEN:
        raise HTTPException(status_code=400, detail="GitHub token not configured")
    
    from src.config.database import SessionLocal
    from src.services.sync_service import SyncService
    
    def run_sync():
        db = SessionLocal()
        try:
            sync_service = SyncService(db)
            import asyncio
            asyncio.run(sync_service.sync_github())
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    background_tasks.add_task(run_sync)
    return {"message": "GitHub sync triggered", "status": "processing"}


@router.post("/webhook")
async def github_webhook(request: Dict[str, Any]):
    """
    Handle GitHub webhook events.
    
    GitHub sends webhooks for events like:
    - push
    - pull_request
    - issues
    - release
    - etc.
    """
    # In production, validate webhook signature
    # from src.integrations.github.webhook_validator import validate_github_signature
    # signature = request.headers.get("X-Hub-Signature-256")
    # if not validate_github_signature(await request.body(), signature, WEBHOOK_SECRET):
    #     raise HTTPException(status_code=401, detail="Invalid webhook signature")
    
    event_type = request.get("action")
    
    if "commits" in request:
        # Push event
        commits = request.get("commits", [])
        return {"message": "Push event processed", "commits_count": len(commits)}
    
    elif "pull_request" in request:
        # Pull request event
        pr = request.get("pull_request", {})
        return {"message": "Pull request event processed", "pr_number": pr.get("number")}
    
    elif "issue" in request:
        # Issue event
        issue = request.get("issue", {})
        return {"message": "Issue event processed", "issue_number": issue.get("number")}
    
    else:
        return {"message": "Webhook event received", "status": "acknowledged"}

