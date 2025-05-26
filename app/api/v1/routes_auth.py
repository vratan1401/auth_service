from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.user import UserCreate, UserOut
from app.schemas.token import SignInRequest, Token, RefreshTokenRequest
from app.services.user_service import signup_user, authenticate_user, logout_user, refresh_access_token

router = APIRouter()

@router.post("/signup", response_model=UserOut)
async def register_user(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    user_obj = await signup_user(user, background_tasks, db)
    return UserOut.model_validate(user_obj)

@router.post("/signin", response_model=Token)
async def login(credentials: SignInRequest, db: AsyncSession = Depends(get_db)):
    return await authenticate_user(credentials, db)

@router.post("/logout")
async def logout(request: Request):
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = auth_header.split(" ")[1]
    await logout_user(token)
    return {"message": "Logged out successfully"}

@router.post("/refresh", response_model=Token)
async def refresh_token(payload: RefreshTokenRequest):
    return await refresh_access_token(payload.refresh_token)
