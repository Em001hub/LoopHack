"""Deduplication service for entities across sources."""
from sqlalchemy.orm import Session
from src.models.orm import UserORM, ProjectORM, TaskORM
from typing import List, Optional
import difflib


class DeduplicatorService:
    """Service to deduplicate entities from different sources."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_duplicate_users(self, threshold: float = 0.85) -> List[tuple]:
        """
        Find potential duplicate users based on email and name similarity.
        
        Args:
            threshold: Similarity threshold (0-1) for matching
            
        Returns:
            List of tuples containing potential duplicate user IDs
        """
        users = self.db.query(UserORM).all()
        duplicates = []
        
        for i, user1 in enumerate(users):
            for user2 in users[i+1:]:
                # Skip if same source (likely same user)
                if user1.source == user2.source:
                    continue
                
                # Check email similarity
                if user1.email and user2.email:
                    email_similarity = difflib.SequenceMatcher(
                        None, 
                        user1.email.lower(), 
                        user2.email.lower()
                    ).ratio()
                    
                    if email_similarity >= threshold:
                        duplicates.append((user1.id, user2.id, email_similarity))
                        continue
                
                # Check name similarity
                if user1.name and user2.name:
                    name_similarity = difflib.SequenceMatcher(
                        None,
                        user1.name.lower(),
                        user2.name.lower()
                    ).ratio()
                    
                    if name_similarity >= threshold:
                        duplicates.append((user1.id, user2.id, name_similarity))
        
        return duplicates
    
    def find_duplicate_projects(self, threshold: float = 0.85) -> List[tuple]:
        """
        Find potential duplicate projects based on name and key similarity.
        
        Args:
            threshold: Similarity threshold (0-1) for matching
            
        Returns:
            List of tuples containing potential duplicate project IDs
        """
        projects = self.db.query(ProjectORM).all()
        duplicates = []
        
        for i, proj1 in enumerate(projects):
            for proj2 in projects[i+1:]:
                # Skip if same source
                if proj1.source == proj2.source:
                    continue
                
                # Check key similarity (exact match)
                if proj1.key and proj2.key and proj1.key.lower() == proj2.key.lower():
                    duplicates.append((proj1.id, proj2.id, 1.0))
                    continue
                
                # Check name similarity
                if proj1.name and proj2.name:
                    name_similarity = difflib.SequenceMatcher(
                        None,
                        proj1.name.lower(),
                        proj2.name.lower()
                    ).ratio()
                    
                    if name_similarity >= threshold:
                        duplicates.append((proj1.id, proj2.id, name_similarity))
        
        return duplicates
    
    def merge_users(self, primary_id: str, duplicate_id: str):
        """
        Merge duplicate user records.
        
        Args:
            primary_id: ID of the user to keep
            duplicate_id: ID of the user to merge and remove
        """
        # Update all tasks assigned to duplicate user
        self.db.query(TaskORM).filter(
            TaskORM.assignee_id == duplicate_id
        ).update({"assignee_id": primary_id})
        
        # Delete duplicate user
        self.db.query(UserORM).filter(UserORM.id == duplicate_id).delete()
        
        self.db.commit()
    
    def merge_projects(self, primary_id: str, duplicate_id: str):
        """
        Merge duplicate project records.
        
        Args:
            primary_id: ID of the project to keep
            duplicate_id: ID of the project to merge and remove
        """
        # Update all tasks belonging to duplicate project
        self.db.query(TaskORM).filter(
            TaskORM.project_id == duplicate_id
        ).update({"project_id": primary_id})
        
        # Delete duplicate project
        self.db.query(ProjectORM).filter(ProjectORM.id == duplicate_id).delete()
        
        self.db.commit()
