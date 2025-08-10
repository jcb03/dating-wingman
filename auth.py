import os
from typing import Optional
from fastapi import Request
from dotenv import load_dotenv

load_dotenv()

# Bearer tokens for authentication
VALID_BEARER_TOKENS = [
    os.getenv("MCP_BEARER_TOKEN", "puch2024"),
    "wingman123",  # Backup token
    "puch2024"     # Default token
]

def extract_bearer_token(request: Request) -> Optional[str]:
    """Extract bearer token from request headers"""
    
    # Check Authorization header
    auth_header = request.headers.get("authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[7:]  # Remove "Bearer " prefix
    
    # Check X-Auth-Token header
    x_auth_token = request.headers.get("x-auth-token", "")
    if x_auth_token:
        return x_auth_token
    
    # Check for token in query params (for some MCP clients)
    if hasattr(request, 'query_params'):
        token = request.query_params.get("token", "")
        if token:
            return token
    
    # Check if the entire auth header is the token (some clients send it directly)
    if auth_header in VALID_BEARER_TOKENS:
        return auth_header
    
    return None

def verify_bearer_token(request: Request) -> bool:
    """Verify that the request has a valid bearer token"""
    
    token = extract_bearer_token(request)
    
    if not token:
        return False
    
    # Check if token is in the list of valid tokens
    return token in VALID_BEARER_TOKENS

def get_bearer_token_info(token: str) -> dict:
    """Get information about a bearer token"""
    
    if token in VALID_BEARER_TOKENS:
        return {
            "valid": True,
            "token": token,
            "permissions": ["full_access"],
            "source": "ai_wingman_mcp"
        }
    
    return {
        "valid": False,
        "token": token,
        "permissions": [],
        "source": None
    }

def require_auth(func):
    """Decorator to require authentication for MCP endpoints"""
    async def wrapper(request: Request, *args, **kwargs):
        if not verify_bearer_token(request):
            return {
                "error": "Unauthorized",
                "message": "Valid bearer token required",
                "valid_tokens": ["Bearer puch2024", "Bearer wingman123"]
            }
        
        return await func(request, *args, **kwargs)
    
    return wrapper

class AuthManager:
    """Authentication manager for the MCP server"""
    
    def __init__(self):
        self.valid_tokens = VALID_BEARER_TOKENS
    
    def add_token(self, token: str):
        """Add a new valid bearer token"""
        if token not in self.valid_tokens:
            self.valid_tokens.append(token)
    
    def remove_token(self, token: str):
        """Remove a bearer token"""
        if token in self.valid_tokens:
            self.valid_tokens.remove(token)
    
    def verify_request(self, request: Request) -> bool:
        """Verify a request has valid authentication"""
        return verify_bearer_token(request)
    
    def get_token_info(self, token: str) -> dict:
        """Get information about a specific token"""
        return get_bearer_token_info(token)

# Global auth manager instance
auth_manager = AuthManager()
