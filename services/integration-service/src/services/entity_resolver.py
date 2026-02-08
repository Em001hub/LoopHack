"""Entity resolution service to match users across different platforms."""
from typing import List, Optional, Dict, Any
from src.models.unified import User
from sqlalchemy.orm import Session
from src.models.orm import UserORM
import difflib
import logging

logger = logging.getLogger(__name__)


class EntityResolver:
    """Resolve and match entities (users, projects) across different sources."""
    
    def __init__(self, db: Session = None):
        self.db = db
        self.user_mapping: Dict[str, str] = {}  # Maps source_id to canonical_id
    
    def resolve_user(self, user: User, existing_users: List[User]) -> Optional[User]:
        """
        Attempt to find a matching user in the existing users list.
        Prioritizes email matching, then falls back to name similarity.
        
        Args:
            user: User to resolve
            existing_users: List of existing users to match against
            
        Returns:
            Matching user if found, None otherwise
        """
        # 1. Exact email match (most reliable)
        if user.email:
            for existing in existing_users:
                if existing.email and existing.email.lower() == user.email.lower():
                    logger.info(f"Matched user by email: {user.email}")
                    return existing
        
        # 2. Email domain + name similarity (for different email addresses same person)
        if user.email and user.name:
            user_domain = user.email.split('@')[1] if '@' in user.email else None
            for existing in existing_users:
                if existing.email and existing.name:
                    existing_domain = existing.email.split('@')[1] if '@' in existing.email else None
                    if user_domain == existing_domain:
                        name_similarity = difflib.SequenceMatcher(
                            None, 
                            user.name.lower(), 
                            existing.name.lower()
                        ).ratio()
                        if name_similarity > 0.85:
                            logger.info(f"Matched user by domain + name: {user.name}")
                            return existing
        
        # 3. Name similarity (fuzzy matching)
        if user.name:
            matches = []
            for existing in existing_users:
                if existing.name:
                    similarity = difflib.SequenceMatcher(
                        None, 
                        user.name.lower(), 
                        existing.name.lower()
                    ).ratio()
                    if similarity > 0.85:
                        matches.append((similarity, existing))
            
            if matches:
                # Return the best match
                matches.sort(key=lambda x: x[0], reverse=True)
                logger.info(f"Matched user by name similarity: {user.name} (score: {matches[0][0]:.2f})")
                return matches[0][1]
        
        return None
    
    def merge_users(self, primary: User, secondary: User) -> User:
        """
        Merge secondary user information into the primary user metadata.
        
        Args:
            primary: Primary user to keep
            secondary: Secondary user to merge into primary
            
        Returns:
            Merged user with combined metadata
        """
        merged_metadata = {**primary.metadata, **secondary.metadata}
        
        # Store cross-platform IDs
        merged_metadata[f"{secondary.source}_id"] = secondary.id
        merged_metadata[f"{secondary.source}_email"] = secondary.email
        
        return User(
            id=primary.id,
            email=primary.email or secondary.email,
            name=primary.name or secondary.name,
            source=primary.source,
            metadata=merged_metadata
        )
    
    def resolve_user_from_db(self, user: User) -> Optional[str]:
        """
        Resolve a user against the database and return canonical user ID.
        
        Args:
            user: User to resolve
            
        Returns:
            Canonical user ID if match found, None otherwise
        """
        if not self.db:
            return None
        
        # Check if we've already resolved this user
        cache_key = f"{user.source}:{user.id}"
        if cache_key in self.user_mapping:
            return self.user_mapping[cache_key]
        
        # Query database for potential matches
        existing_users = self.db.query(UserORM).all()
        
        # Convert ORM to unified model
        unified_users = [
            User(
                id=u.id,
                email=u.email,
                name=u.name,
                source=u.source,
                metadata=u.metadata_json or {}
            )
            for u in existing_users
        ]
        
        # Attempt to resolve
        matched_user = self.resolve_user(user, unified_users)
        
        if matched_user:
            # Cache the mapping
            self.user_mapping[cache_key] = matched_user.id
            return matched_user.id
        
        return None
    
    def create_canonical_user_id(self, user: User) -> str:
        """
        Create a canonical user ID from email or name.
        
        Args:
            user: User to create ID for
            
        Returns:
            Canonical user ID
        """
        if user.email:
            # Use email as base for canonical ID
            return f"user_{user.email.lower().replace('@', '_at_').replace('.', '_')}"
        elif user.name:
            # Use name as fallback
            return f"user_{user.name.lower().replace(' ', '_')}_{user.source}"
        else:
            # Last resort: use source ID
            return f"user_{user.source}_{user.id}"

