"""Sync service to orchestrate data synchronization from external sources."""
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
from typing import List, Dict, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class SyncService:
    """Service to synchronize data from external integrations."""
    
    def __init__(self, db: Session):
        self.db = db
        self.sync_stats = {
            "projects": {"created": 0, "updated": 0, "errors": 0},
            "tasks": {"created": 0, "updated": 0, "errors": 0},
            "users": {"created": 0, "updated": 0, "errors": 0},
            "events": {"created": 0, "updated": 0, "errors": 0}
        }

    def _upsert_user(self, user: User):
        """Upsert user with error handling."""
        try:
            existing = self.db.query(UserORM).filter(UserORM.id == user.id).first()
            if existing:
                existing.email = user.email
                existing.name = user.name
                existing.metadata_json = user.metadata
                self.sync_stats["users"]["updated"] += 1
                logger.debug(f"Updated user: {user.id}")
            else:
                new_user = UserORM(
                    id=user.id,
                    email=user.email,
                    name=user.name,
                    source=user.source,
                    metadata_json=user.metadata
                )
                self.db.add(new_user)
                self.sync_stats["users"]["created"] += 1
                logger.debug(f"Created user: {user.id}")
        except Exception as e:
            self.sync_stats["users"]["errors"] += 1
            logger.error(f"Error upserting user {user.id}: {str(e)}")

    def _upsert_project(self, project: Project):
        """Upsert project with error handling."""
        try:
            existing = self.db.query(ProjectORM).filter(ProjectORM.id == project.id).first()
            if existing:
                existing.name = project.name
                existing.key = project.key
                existing.metadata_json = project.metadata
                self.sync_stats["projects"]["updated"] += 1
                logger.debug(f"Updated project: {project.id}")
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
                self.sync_stats["projects"]["created"] += 1
                logger.debug(f"Created project: {project.id}")
        except Exception as e:
            self.sync_stats["projects"]["errors"] += 1
            logger.error(f"Error upserting project {project.id}: {str(e)}")

    def _upsert_task(self, task: Task):
        """Upsert task with error handling."""
        try:
            existing = self.db.query(TaskORM).filter(TaskORM.id == task.id).first()
            if existing:
                existing.status = task.status
                existing.updated_at = task.updated_at
                existing.metadata_json = task.metadata
                self.sync_stats["tasks"]["updated"] += 1
                logger.debug(f"Updated task: {task.id}")
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
                self.sync_stats["tasks"]["created"] += 1
                logger.debug(f"Created task: {task.id}")
        except Exception as e:
            self.sync_stats["tasks"]["errors"] += 1
            logger.error(f"Error upserting task {task.id}: {str(e)}")

    async def sync_all(self) -> Dict[str, Any]:
        """
        Main sync orchestrator.
        Syncs all configured integrations and returns statistics.
        
        Returns:
            Dictionary with sync statistics
        """
        logger.info("Starting full sync of all integrations")
        start_time = datetime.utcnow()
        
        try:
            # 1. Sync Jira
            await self.sync_jira()
            
            # 2. Sync GitHub
            await self.sync_github()
            
            # 3. Sync Slack
            await self.sync_slack()
            
            # 4. Sync Calendar
            await self.sync_calendar()
            
            self.db.commit()
            
            end_time = datetime.utcnow()
            duration = (end_time - start_time).total_seconds()
            
            logger.info(f"Full sync completed in {duration:.2f}s")
            logger.info(f"Sync stats: {self.sync_stats}")
            
            return {
                "status": "success",
                "duration_seconds": duration,
                "stats": self.sync_stats,
                "timestamp": end_time.isoformat()
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Sync failed: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "error": str(e),
                "stats": self.sync_stats
            }

    async def sync_jira(self):
        """Sync Jira projects and issues."""
        domain = os.getenv("JIRA_DOMAIN")
        email = os.getenv("JIRA_EMAIL")
        token = os.getenv("JIRA_API_TOKEN")
        
        if not all([domain, email, token]):
            logger.warning("Jira credentials not configured, skipping sync")
            return

        logger.info("Starting Jira sync")
        try:
            client = JiraClient(domain, email, token)
            raw_projects = await client.get_projects()
            
            for rp in raw_projects:
                try:
                    project = parse_jira_project(rp)
                    self._upsert_project(project)
                    
                    # Fetch issues for this project
                    raw_issues = await client.get_issues(project.key)
                    for ri in raw_issues:
                        task = parse_jira_issue(ri, project.id)
                        self._upsert_task(task)
                        
                except Exception as e:
                    logger.error(f"Error syncing Jira project {rp.get('key', 'unknown')}: {str(e)}")
                    
            logger.info(f"Jira sync completed: {len(raw_projects)} projects processed")
            
        except Exception as e:
            logger.error(f"Jira sync failed: {str(e)}", exc_info=True)

    async def sync_github(self):
        """Sync GitHub repositories."""
        token = os.getenv("GITHUB_TOKEN")
        
        if not token:
            logger.warning("GitHub token not configured, skipping sync")
            return

        logger.info("Starting GitHub sync")
        try:
            client = GitHubClient(token)
            raw_repos = await client.get_repositories()
            
            for rr in raw_repos:
                try:
                    project = parse_github_repo(rr)
                    self._upsert_project(project)
                except Exception as e:
                    logger.error(f"Error syncing GitHub repo {rr.get('name', 'unknown')}: {str(e)}")
            
            logger.info(f"GitHub sync completed: {len(raw_repos)} repositories processed")
            
        except Exception as e:
            logger.error(f"GitHub sync failed: {str(e)}", exc_info=True)

    async def sync_slack(self):
        """Sync Slack users and channels."""
        token = os.getenv("SLACK_TOKEN")
        
        if not token:
            logger.warning("Slack token not configured, skipping sync")
            return

        logger.info("Starting Slack sync")
        try:
            client = SlackClient(token)
            raw_users = await client.get_users()
            
            for ru in raw_users:
                try:
                    user = parse_slack_user(ru)
                    self._upsert_user(user)
                except Exception as e:
                    logger.error(f"Error syncing Slack user {ru.get('id', 'unknown')}: {str(e)}")
            
            logger.info(f"Slack sync completed: {len(raw_users)} users processed")
            
        except Exception as e:
            logger.error(f"Slack sync failed: {str(e)}", exc_info=True)

    async def sync_calendar(self):
        """Sync Google Calendar events."""
        token = os.getenv("GOOGLE_ACCESS_TOKEN")
        
        if not token:
            logger.warning("Google Calendar token not configured, skipping sync")
            return

        logger.info("Starting Google Calendar sync")
        try:
            client = GoogleCalendarClient(access_token=token)
            raw_events = await client.get_events()
            
            for re in raw_events:
                try:
                    event = parse_calendar_event(re)
                    # Store event in database (EventORM logic would go here)
                    logger.debug(f"Processed calendar event: {event.id}")
                except Exception as e:
                    logger.error(f"Error syncing calendar event: {str(e)}")
            
            logger.info(f"Calendar sync completed: {len(raw_events)} events processed")
            
        except Exception as e:
            logger.error(f"Calendar sync failed: {str(e)}", exc_info=True)

