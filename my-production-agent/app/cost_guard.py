import redis
from datetime import datetime
from fastapi import HTTPException, Depends
from .config import settings
from .auth import verify_api_key

r = redis.from_url(settings.REDIS_URL)

def check_budget(user_id: str = Depends(verify_api_key)):
    month_key = datetime.now().strftime("%Y-%m")
    key = f"budget:{user_id}:{month_key}"
    
    current = float(r.get(key) or 0)
    if current >= settings.MONTHLY_BUDGET_USD:
        raise HTTPException(status_code=402, detail="Monthly budget exceeded. Upgrade your plan.")

def record_cost(user_id: str, cost: float):
    month_key = datetime.now().strftime("%Y-%m")
    key = f"budget:{user_id}:{month_key}"
    r.incrbyfloat(key, cost)
    r.expire(key, 32 * 24 * 3600)
