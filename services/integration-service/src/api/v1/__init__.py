from fastapi import APIRouter
from src.api.v1.endpoints import projects, tasks, users, events, sync
from src.api.v1.webhooks import jira, github, slack, calendar

api_router = APIRouter()
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(sync.router, prefix="/sync", tags=["sync"])

api_router.include_router(jira.router, prefix="/webhooks/jira", tags=["webhooks"])
api_router.include_router(github.router, prefix="/webhooks/github", tags=["webhooks"])
api_router.include_router(slack.router, prefix="/webhooks/slack", tags=["webhooks"])
api_router.include_router(calendar.router, prefix="/webhooks/calendar", tags=["webhooks"])
