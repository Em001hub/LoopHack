from sqlalchemy.orm import Session
from src.models.orm import UserORM, ProjectORM, TaskORM, EventORM
from src.models.unified import User, Project, Task, Event
from src.integrations.jira.client import JiraClient
from src.integrations.github.client import GitHubClient
from src.integrations.slack.client import SlackClient
from src.integrations.google_calendar.client import GoogleCalendarClient
from src.integrations.jira.parser import parse_jira_project, parse_jira_issue, parse_jira_user
from src.integrations.github.parser import parse_github_repo, parse_github_commit, parse_github_pr
from src.integrations.slack.parser import parse_slack_channel, parse_slack_message, parse_slack_user
from src.integrations.google_calendar.parser import parse_calendar_event
import os
from typing import List

class SyncService:
    def __init__(self, db: Session):
        self.db = db

    def _upsert_user(self, user: User):
        existing = self.db.query(UserORM).filter(UserORM.id == user.id).first()
        if existing:
            existing.email = user.email
            existing.name = user.name
            existing.metadata_json = user.metadata
        else:
            new_user = UserORM(
                id=user.id,
                email=user.email,
                name=user.name,
                source=user.source,
                metadata_json=user.metadata
            )
            self.db.add(new_user)

    def _upsert_project(self, project: Project):
        existing = self.db.query(ProjectORM).filter(ProjectORM.id == project.id).first()
        if existing:
            existing.name = project.name
            existing.key = project.key
            existing.metadata_json = project.metadata
        else:
            new_proj = ProjectORM(
                id=project.id,
                name=project.name,
                key=project.key,
                source=project.source,
                url=project.url,
                metadata_json=project.metadata
            )
            self.db.add(new_proj)

    def _upsert_task(self, task: Task):
        existing = self.db.query(TaskORM).filter(TaskORM.id == task.id).first()
        if existing:
            existing.status = task.status
            existing.updated_at = task.updated_at
            existing.metadata_json = task.metadata
        else:
            new_task = TaskORM(
                id=task.id,
                project_id=task.project_id,
                title=task.title,
                status=task.status,
                created_at=task.created_at,
                updated_at=task.updated_at,
                source=task.source,
                metadata_json=task.metadata
            )
            self.db.add(new_task)

    async def sync_all(self):
        """
        Main sync orchestrator.
        In a production app, these would be separate background tasks.
        """
        # 1. Sync Jira
        await self.sync_jira()
        # 2. Sync GitHub
        await self.sync_github()
        # 3. Sync Slack
        await self.sync_slack()
        # 4. Sync Calendar
        await self.sync_calendar()
        
        self.db.commit()

    async def sync_jira(self):
        domain = os.getenv("JIRA_DOMAIN")
        email = os.getenv("JIRA_EMAIL")
        token = os.getenv("JIRA_API_TOKEN")
        if not all([domain, email, token]): return

        client = JiraClient(domain, email, token)
        raw_projects = await client.get_projects()
        for rp in raw_projects:
            project = parse_jira_project(rp)
            self._upsert_project(project)
            
            raw_issues = await client.get_issues(project.key)
            for ri in raw_issues:
                task = parse_jira_issue(ri, project.id)
                self._upsert_task(task)

    async def sync_github(self):
        token = os.getenv("GITHUB_TOKEN")
        if not token: return

        client = GitHubClient(token)
        raw_repos = await client.get_repositories()
        for rr in raw_repos:
            project = parse_github_repo(rr)
            self._upsert_project(project)
            # Fetch commits and PRs as needed...

    async def sync_slack(self):
        token = os.getenv("SLACK_TOKEN")
        if not token: return

        client = SlackClient(token)
        raw_users = await client.get_users()
        for ru in raw_users:
            user = parse_slack_user(ru)
            self._upsert_user(user)

    async def sync_calendar(self):
        token = os.getenv("GOOGLE_ACCESS_TOKEN")
        if not token: return

        client = GoogleCalendarClient(access_token=token)
        raw_events = await client.get_events()
        for re in raw_events:
            event = parse_calendar_event(re)
            # Persistent event ORM logic...
            pass
