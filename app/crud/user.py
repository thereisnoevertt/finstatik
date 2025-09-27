from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.profile import Profile
from app.core.security import hash_password


async def get_user_by_email(email: str, session: AsyncSession):
    q = select(User).where(User.email == email)
    r = await session.execute(q)
    return r.scalars().first()


async def create_user(email: str, display_name: str, password: str, session: AsyncSession):
    user = User(email=email, display_name=display_name, password_hash=hash_password(password))
    session.add(user)
    await session.flush()
    profile = Profile(user_id=user.id, coins=0, streak=0, rating_points=0)
    session.add(profile)
    await session.commit()
    await session.refresh(user)
    return user