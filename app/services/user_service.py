from fastapi import HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from jose import JWTError

from app.core.security import verify_password, hash_password
from app.core.jwt import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
)
from app.schemas.token import SignInRequest, Token
from app.db.crud import get_user_by_email, create_user
from app.services.cache_service import cache_user
from app.db.redis import redis_client
from app.schemas.user import UserCreate
from app.db.models import User

ACCESS_EXPIRE_MINUTES = 15

async def signup_user(user: UserCreate, background_tasks: BackgroundTasks, db: AsyncSession) -> User:
    existing_user = await get_user_by_email(user.email, db)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    user_data = user.dict()
    user_data["password"] = hash_password(user.password)
    new_user = await create_user(user_data, db)

    background_tasks.add_task(cache_user, {
        "id": str(new_user.id),
        "name": new_user.name,
        "email": new_user.email,
        "phone": new_user.phone,
        "created_time": new_user.created_time.isoformat()
    })

    return new_user

async def authenticate_user(credentials: SignInRequest, db: AsyncSession) -> Token:
    user = await get_user_by_email(credentials.email, db)
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    data = {"sub": user.email}
    access_token = create_access_token(data, expires_delta=timedelta(minutes=ACCESS_EXPIRE_MINUTES))
    refresh_token = create_refresh_token(data)

    return Token(access_token=access_token, refresh_token=refresh_token)

async def logout_user(token: str):
    try:
        payload = decode_access_token(token)
        exp = payload.get("exp")
        ttl = exp - int(datetime.utcnow().timestamp())
        await redis_client.setex(f"bl:{token}", ttl, "blacklisted")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid token")

async def refresh_access_token(refresh_token: str) -> Token:
    try:
        payload = decode_access_token(refresh_token)
        email = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access = create_access_token({"sub": email}, expires_delta=timedelta(minutes=ACCESS_EXPIRE_MINUTES))
    new_refresh = create_refresh_token({"sub": email})

    return Token(access_token=new_access, refresh_token=new_refresh)
