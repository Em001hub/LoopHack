from typing import List, Optional
from src.models.unified import User
import difflib

class EntityResolver:
    def __init__(self):
        pass

    def resolve_user(self, user: User, existing_users: List[User]) -> Optional[User]:
        """
        Attempt to find a matching user in the existing users list.
        Prioritizes email matching, then falls back to name similarity.
        """
        # 1. Match by email
        if user.email:
            for existing in existing_users:
                if existing.email.lower() == user.email.lower():
                    return existing

        # 2. Match by name similarity (fuzzy matching)
        if user.name:
            matches = []
            for existing in existing_users:
                if existing.name:
                    similarity = difflib.SequenceMatcher(None, user.name.lower(), existing.name.lower()).ratio()
                    if similarity > 0.85:
                        matches.append((similarity, existing))
            
            if matches:
                # Return the best match
                matches.sort(key=lambda x: x[0], reverse=True)
                return matches[0][1]

        return None

    def merge_users(self, primary: User, secondary: User) -> User:
        """
        Merge secondary user information into the primary user metadata.
        """
        merged_metadata = {**primary.metadata, **secondary.metadata}
        merged_metadata[f"{secondary.source}_id"] = secondary.id
        
        return User(
            id=primary.id,
            email=primary.email or secondary.email,
            name=primary.name or secondary.name,
            source=primary.source,
            metadata=merged_metadata
        )
