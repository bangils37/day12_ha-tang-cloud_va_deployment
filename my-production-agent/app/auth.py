from fastapi import Header, HTTPException
from .config import settings

def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")):
    if x_api_key != settings.AGENT_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    # Return a mock user_id based on the valid API key
    return f"user_{x_api_key[-4:]}"
