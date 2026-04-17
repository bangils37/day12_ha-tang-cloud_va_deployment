import time
import json
import logging
import redis
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from .config import settings
from .auth import verify_api_key
from .rate_limiter import check_rate_limit
from .cost_guard import check_budget
from utils.mock_llm import ask

# Cấu hình Structured Logging
logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s", "level":"%(levelname)s", "msg":%(message)s}'
)
logger = logging.getLogger(__name__)

# Kết nối Redis cho conversation history
r = redis.from_url(settings.REDIS_URL, decode_responses=True)

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

@app.get("/health")
def health():
    """Liveness probe"""
    return {"status": "ok", "timestamp": time.time()}

@app.get("/ready")
def ready():
    """Readiness probe - Kiểm tra kết nối Redis"""
    try:
        r.ping()
        return {"status": "ready"}
    except Exception as e:
        logger.error(json.dumps({"event": "readiness_failed", "error": str(e)}))
        raise HTTPException(status_code=503, detail="Redis not available")

@app.post("/ask")
async def ask_endpoint(
    request: Request,
    user_id: str = Depends(verify_api_key)
):
    # 1. Check Rate Limit & Budget
    await check_rate_limit(user_id)
    await check_budget(user_id)

    # 2. Parse request
    try:
        body = await request.json()
        question = body.get("question")
    except:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    if not question:
        raise HTTPException(status_code=422, detail="Question is required")

    # 3. Get History from Redis
    history_key = f"history:{user_id}"
    history = r.lrange(history_key, -10, -1) # Lấy 10 câu gần nhất

    # 4. Call LLM (Mock)
    logger.info(json.dumps({
        "event": "llm_call",
        "user_id": user_id,
        "question": question
    }))
    
    response = ask(question)

    # 5. Save to Redis (Stateless design)
    r.rpush(history_key, json.dumps({"q": question, "a": response}))
    r.ltrim(history_key, -20, -1) # Giữ tối đa 20 câu
    r.expire(history_key, 3600)   # Hết hạn sau 1h

    return {
        "answer": response,
        "history_count": len(history),
        "user_id": user_id
    }

@app.on_event("shutdown")
def shutdown_event():
    """Graceful shutdown"""
    logger.info(json.dumps({"event": "shutdown", "msg": "Agent is shutting down gracefully"}))
    # Close connections if any
