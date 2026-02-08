from fastapi import APIRouter, HTTPException
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
