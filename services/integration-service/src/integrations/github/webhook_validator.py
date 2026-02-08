"""GitHub webhook signature validation."""
import hmac
import hashlib
from typing import Optional


def validate_github_signature(payload: bytes, signature_header: str, secret: str) -> bool:
    """
    Validate GitHub webhook signature.
    
    GitHub sends the signature in the X-Hub-Signature-256 header as:
    sha256=<signature>
    
    Args:
        payload: Raw request body as bytes
        signature_header: Value from X-Hub-Signature-256 header
        secret: Webhook secret configured in GitHub
        
    Returns:
        True if signature is valid, False otherwise
    """
    if not signature_header or not signature_header.startswith('sha256='):
        return False
    
    # Extract the signature from the header
    expected_signature = signature_header.split('=')[1]
    
    # Compute the HMAC signature
    computed_signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    # Compare signatures (constant-time comparison to prevent timing attacks)
    return hmac.compare_digest(computed_signature, expected_signature)


def validate_github_signature_sha1(payload: bytes, signature_header: str, secret: str) -> bool:
    """
    Validate GitHub webhook signature using SHA1 (legacy).
    
    Args:
        payload: Raw request body as bytes
        signature_header: Value from X-Hub-Signature header
        secret: Webhook secret configured in GitHub
        
    Returns:
        True if signature is valid, False otherwise
    """
    if not signature_header or not signature_header.startswith('sha1='):
        return False
    
    expected_signature = signature_header.split('=')[1]
    
    computed_signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha1
    ).hexdigest()
    
    return hmac.compare_digest(computed_signature, expected_signature)
