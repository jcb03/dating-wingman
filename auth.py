import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

# Bearer tokens for authentication
VALID_BEARER_TOKENS = [
    os.getenv("MCP_BEARER_TOKEN", "puch2024"),
    "wingman123",  # Backup token
    "puch2024"     # Default token
]

def extract_bearer_token(headers: Dict[str, str]) -> Optional[str]:
    """Extract bearer token from request headers"""
    
    # Check Authorization header
    auth_header = headers.get("authorization", "") or headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[7:]  # Remove "Bearer " prefix
    
    # Check X-Auth-Token header
    x_auth_token = headers.get("x-auth-token", "") or headers.get("X-Auth-Token", "")
    if x_auth_token:
        return x_auth_token
    
    # Check if the entire auth header is the token (some clients send it directly)
    if auth_header in VALID_BEARER_TOKENS:
        return auth_header
    
    return None

def verify_bearer_token(headers: Dict[str, str]) -> bool:
    """Verify that the request has a valid bearer token"""
    
    token = extract_bearer_token(headers)
    
    if not token:
        return False
    
    # Check if token is in the list of valid tokens
    return token in VALID_BEARER_TOKENS

def verify_token_string(token: str) -> bool:
    """Verify a token string directly"""
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

def create_auth_error() -> Dict[str, Any]:
    """Create standardized authentication error response"""
    return {
        "error": "Unauthorized",
        "message": "Valid bearer token required",
        "valid_tokens": ["Bearer puch2024", "Bearer wingman123"]
    }

class AuthManager:
    """Authentication manager for the MCP server"""
    
    def __init__(self):
        self.valid_tokens = VALID_BEARER_TOKENS.copy()
    
    def add_token(self, token: str):
        """Add a new valid bearer token"""
        if token not in self.valid_tokens:
            self.valid_tokens.append(token)
    
    def remove_token(self, token: str):
        """Remove a bearer token"""
        if token in self.valid_tokens:
            self.valid_tokens.remove(token)
    
    def verify_headers(self, headers: Dict[str, str]) -> bool:
        """Verify headers have valid authentication"""
        return verify_bearer_token(headers)
    
    def verify_token(self, token: str) -> bool:
        """Verify a token directly"""
        return verify_token_string(token)
    
    def get_token_info(self, token: str) -> dict:
        """Get information about a specific token"""
        return get_bearer_token_info(token)

# Global auth manager instance
auth_manager = AuthManager()

# FastMCP compatible auth functions
def fastmcp_auth_middleware(headers: Dict[str, str]) -> bool:
    """FastMCP compatible authentication middleware"""
    return verify_bearer_token(headers)

def fastmcp_verify_token(token: str) -> bool:
    """FastMCP compatible token verification"""
    return token in VALID_BEARER_TOKENS
