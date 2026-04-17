import redis
import time
from fastapi import HTTPException, Depends
from .config import settings
from .auth import verify_api_key

r = redis.from_url(settings.REDIS_URL)

def check_rate_limit(user_id: str = Depends(verify_api_key)):
    now = time.time()
    window_start = now - 60
    key = f"rate_limit:{user_id}"

    # Remove old requests
    r.zremrangebyscore(key, 0, window_start)

    # Count requests in the current window
    request_count = r.zcard(key)

    if request_count >= settings.RATE_LIMIT_PER_MINUTE:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")

    # Add current request
    r.zadd(key, {str(now): now})
    # Set expiry to clean up memory
    r.expire(key, 60)
