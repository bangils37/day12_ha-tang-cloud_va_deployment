from fastapi import Header, HTTPException, Security
from .config import settings

async def verify_api_key(x_api_key: str = Header(...)):
    """
    Xác thực API Key từ Header.
    Trả về user_id (trong lab này giả định user_id là 'default_user' nếu key đúng).
    """
    if x_api_key != settings.AGENT_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API Key"
        )
    return "user_123"  # Giả định user_id cố định cho demo
