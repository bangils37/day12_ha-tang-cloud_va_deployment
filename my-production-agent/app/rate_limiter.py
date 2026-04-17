import time
import redis
from fastapi import HTTPException
from .config import settings

# Kết nối Redis
r = redis.from_url(settings.REDIS_URL, decode_responses=True)

async def check_rate_limit(user_id: str):
    """
    Sử dụng thuật toán Sliding Window với Redis Sorted Set.
    Giới hạn: 10 requests / phút.
    """
    now = time.time()
    key = f"rate_limit:{user_id}"
    window_start = now - 60

    # Pipeline để đảm bảo tính nguyên tử
    pipe = r.pipeline()
    pipe.zremrangebyscore(key, 0, window_start)  # Xóa các request cũ hơn 1 phút
    pipe.zcard(key)                              # Đếm số request trong window
    pipe.zadd(key, {str(now): now})              # Thêm request hiện tại
    pipe.expire(key, 60)                         # Set TTL
    results = pipe.execute()

    request_count = results[1]

    if request_count >= settings.RATE_LIMIT_PER_MINUTE:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Rate limit exceeded",
                "limit": settings.RATE_LIMIT_PER_MINUTE,
                "window": "60s"
            }
        )
    return True
