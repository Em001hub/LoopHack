"""Jira webhook signature validation."""
import hmac
import hashlib
import base64
from typing import Optional


def validate_jira_signature(payload: bytes, signature_header: str, secret: str) -> bool:
    """
    Validate Jira webhook signature.
    
    Jira Cloud uses JWT tokens for webhook authentication, but for simplicity
    we can use HMAC-based validation for self-hosted Jira or custom setups.
    
    Args:
        payload: Raw request body as bytes
        signature_header: Signature from request header
        secret: Webhook secret
        
    Returns:
        True if signature is valid, False otherwise
    """
    if not signature_header or not secret:
        return False
    
    # Compute HMAC-SHA256 signature
    computed_signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).digest()
    
    # Base64 encode the signature
    computed_signature_b64 = base64.b64encode(computed_signature).decode('utf-8')
    
    # Compare signatures
    return hmac.compare_digest(computed_signature_b64, signature_header)


def validate_jira_query_token(query_token: str, expected_token: str) -> bool:
    """
    Validate Jira webhook using query token method.
    
    Some Jira webhooks include a token in the query string.
    
    Args:
        query_token: Token from query string
        expected_token: Expected token value
        
    Returns:
        True if tokens match, False otherwise
    """
    if not query_token or not expected_token:
        return False
    
    return hmac.compare_digest(query_token, expected_token)
