from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserOut
from app.services.cache_service import get_cached_user
from app.db import crud
from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.get("/user", response_model=UserOut)
async def get_user(
    current_user: UserOut = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    email = current_user.email

    cached_user = await get_cached_user(email)
    if cached_user:
        return cached_user

    user = await crud.get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")


    user_out = UserOut.model_validate(user)
    return user_out
