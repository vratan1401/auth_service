from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import User

async def get_user_by_email(email: str, session: AsyncSession):
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def create_user(user_data, session: AsyncSession):
    new_user = User(**user_data)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user
