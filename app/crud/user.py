from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.profile import Profile

async def get_user_by_username(username: str, session: AsyncSession):
    """Получить пользователя по username"""
    q = select(User).where(User.username == username)
    r = await session.execute(q)
    return r.scalars().first()

async def get_user_by_email(email: str, session: AsyncSession):
    """Получить пользователя по email"""
    q = select(User).where(User.email == email)
    r = await session.execute(q)
    return r.scalars().first()

async def create_user(
    username: str, 
    email: str, 
    first_name: str,
    last_name: str,
    password: str, 
    session: AsyncSession
):
    """Создать нового пользователя"""
    user = User(
        username=username,
        email=email,
        password=password,  # БЕЗ хеширования
        avatar_url=None
    )
    session.add(user)
    await session.flush()
    
    profile = Profile(
        user_id=user.id,
        first_name=first_name,
        last_name=last_name,
        coins=0, 
        streak=0, 
        rating_points=0,
        level="Новичок"
    )
    session.add(profile)
    await session.commit()
    await session.refresh(user)
    return user