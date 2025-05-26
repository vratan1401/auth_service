from fastapi import Depends, HTTPException
from jose import JWTError
from app.core.jwt import decode_access_token
from app.core.oauth2 import oauth2_scheme
from app.db.crud import get_user_by_email
from app.db.redis import redis_client
from app.dependencies.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserOut

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> UserOut:
    blacklisted = await redis_client.get(f"bl:{token}")
    if blacklisted:
        raise HTTPException(status_code=401, detail="Token is blacklisted")

    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
