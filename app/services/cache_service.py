import json
from app.db.redis import redis_client

async def cache_user(user_data: dict):
    key = f"user:{user_data['email']}"
    await redis_client.set(key, json.dumps(user_data))

async def get_cached_user(email: str):
    key = f"user:{email}"
    data = await redis_client.get(key)
    if data:
        return json.loads(data)
    return None
