import redis
from datetime import datetime
from fastapi import HTTPException
from .config import settings

r = redis.from_url(settings.REDIS_URL, decode_responses=True)

async def check_budget(user_id: str):
    """
    Kiểm tra ngân sách hàng tháng của user.
    Giới hạn: $10/tháng.
    """
    month_key = datetime.now().strftime("%Y-%m")
    key = f"budget:{user_id}:{month_key}"
    
    current_spending = float(r.get(key) or 0)
    
    if current_spending + settings.COST_PER_REQUEST > settings.MONTHLY_BUDGET_USD:
        raise HTTPException(
            status_code=402,
            detail={
                "error": "Monthly budget exceeded",
                "budget": settings.MONTHLY_BUDGET_USD,
                "current": current_spending
            }
        )
    
    # Tăng ngân sách sau khi check thành công (thực tế nên tăng sau khi gọi LLM)
    r.incrbyfloat(key, settings.COST_PER_REQUEST)
    r.expire(key, 32 * 24 * 3600)  # 32 ngày để cover hết tháng
    
    return True
