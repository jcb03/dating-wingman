import os
from typing import Set

def allowed_tokens() -> Set[str]:
    raw = os.getenv("MCP_BEARER_TOKENS", "")
    toks = [t.strip() for t in raw.split(",") if t.strip()]
    return set(toks)

def check_bearer(token: str) -> bool:
    return token in allowed_tokens()
