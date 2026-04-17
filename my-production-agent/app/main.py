import signal
import sys
import logging
import json
from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
import redis
from .config import settings
from .auth import verify_api_key
from .rate_limiter import check_rate_limit
from .cost_guard import check_budget, record_cost

# Configure structured JSON logging
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "level": record.levelname,
            "message": record.getMessage(),
            "name": record.name
        }
        return json.dumps(log_obj)

logger = logging.getLogger()
# remove default handlers
for h in logger.handlers:
    logger.removeHandler(h)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(settings.LOG_LEVEL)

app = FastAPI()
r = redis.from_url(settings.REDIS_URL)
is_shutting_down = False

def shutdown_handler(signum, frame):
    global is_shutting_down
    logger.info("Received shutdown signal. Stopping new requests.")
    is_shutting_down = True
    # Uvicorn handles the rest

signal.signal(signal.SIGTERM, shutdown_handler)

@app.middleware("http")
async def reject_if_shutting_down(request, call_next):
    if is_shutting_down:
        return JSONResponse(status_code=503, content={"detail": "Service is shutting down"})
    response = await call_next(request)
    return response

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ready")
def ready():
    try:
        r.ping()
        return {"status": "ready"}
    except Exception as e:
        logger.error(f"Redis connection failed: {e}")
        return JSONResponse(
            status_code=503,
            content={"status": "not ready"}
        )

@app.post("/ask")
def ask(
    question: str = Body(..., embed=True),
    user_id: str = Depends(verify_api_key),
    _rate_limit: None = Depends(check_rate_limit),
    _budget: None = Depends(check_budget)
):
    history_key = f"history:{user_id}"
    # get history from redis
    history = [h.decode('utf-8') for h in r.lrange(history_key, 0, -1)]
    
    logger.info(f"Processing question from {user_id}")
    answer = f"Agent response to: {question}"
    
    r.rpush(history_key, f"User: {question}")
    r.rpush(history_key, f"Agent: {answer}")
    r.expire(history_key, 3600 * 24)
    
    record_cost(user_id, 0.001)
    
    return {"question": question, "answer": answer, "history_len": len(history) // 2 + 1}
