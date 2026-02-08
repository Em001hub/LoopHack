"""Base integration class with common functionality."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class BaseIntegration(ABC):
    """Base class for all external integrations."""
    
    def __init__(self, credentials: Dict[str, str]):
        """
        Initialize the integration with credentials.
        
        Args:
            credentials: Dictionary containing authentication credentials
        """
        self.credentials = credentials
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    @abstractmethod
    async def test_connection(self) -> bool:
        """
        Test if the connection to the external service is valid.
        
        Returns:
            True if connection is successful, False otherwise
        """
        pass
    
    @abstractmethod
    async def sync(self) -> Dict[str, Any]:
        """
        Perform a full sync of data from the external service.
        
        Returns:
            Dictionary with sync results (counts, errors, etc.)
        """
        pass
    
    @abstractmethod
    def validate_webhook(self, payload: bytes, signature: str) -> bool:
        """
        Validate webhook signature from the external service.
        
        Args:
            payload: Raw webhook payload
            signature: Signature header from the webhook
            
        Returns:
            True if signature is valid, False otherwise
        """
        pass
    
    def log_error(self, message: str, error: Exception):
        """Log an error with context."""
        self.logger.error(f"{message}: {str(error)}", exc_info=True)
    
    def log_info(self, message: str):
        """Log an info message."""
        self.logger.info(message)
    
    def log_warning(self, message: str):
        """Log a warning message."""
        self.logger.warning(message)
