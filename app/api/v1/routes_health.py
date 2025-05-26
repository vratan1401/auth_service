from fastapi import APIRouter
from app.db.redis import redis_client
router = APIRouter()

@router.get("/health")
async def health_check():
    try:
        pong = await redis_client.ping()
        return {"status": "ok", "redis": pong}
    except Exception as e:
        return {"status": "ok", "redis": "unreachable", "error": str(e)}

@router.get("/redis/set")
async def set_redis_key():
    await redis_client.set("hello", "vaibhav")
    return {"message": "Key set"}

@router.get("/redis/get")
async def get_redis_key():
    value = await redis_client.get("hello")
    return {"hello": value}