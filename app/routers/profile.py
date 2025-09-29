from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.db.session import get_session
from app.schemas.profile import ProfileOut, ProfileFullOut
from app.models.profile import Profile
from app.models.user import User
from app.models.module import Module
from app.models.lesson import Lesson
from app.dependencies import get_current_user

router = APIRouter(prefix="/profile", tags=["profile"])

@router.get("/me", response_model=ProfileOut)
async def get_profile(
    user: User = Depends(get_current_user), 
    session: AsyncSession = Depends(get_session)
):
    """Базовая информация профиля"""
    profile = await session.get(Profile, user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.get("/me/full", response_model=ProfileFullOut)
async def get_full_profile(
    user: User = Depends(get_current_user), 
    session: AsyncSession = Depends(get_session)
):
    """Полная информация профиля"""
    from sqlalchemy import text
    
    profile = await session.get(Profile, user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Подсчет статистики
    completed_modules_result = await session.execute(
        text("""
            SELECT COUNT(DISTINCT l.module_id)
            FROM user_lessons ul
            JOIN lessons l ON ul.lesson_id = l.id
            WHERE ul.user_id = :uid
        """),
        {"uid": user.id}
    )
    completed_modules = completed_modules_result.scalar() or 0
    
    total_modules_result = await session.execute(select(func.count(Module.id)))
    total_modules = total_modules_result.scalar() or 0
    
    achievements_count = completed_modules
    
    completed_lessons_result = await session.execute(
        text("SELECT COUNT(*) FROM user_lessons WHERE user_id = :uid"),
        {"uid": user.id}
    )
    completed_lessons = completed_lessons_result.scalar() or 0
    
    total_lessons_result = await session.execute(select(func.count(Lesson.id)))
    total_lessons = total_lessons_result.scalar() or 1
    
    progress_percent = int((completed_lessons / total_lessons * 100)) if total_lessons > 0 else 0
    
    # Генерация аватара
    avatar_url = user.avatar_url
    if not avatar_url:
        initials = f"{profile.first_name[0]}{profile.last_name[0]}".upper()
        avatar_url = f"https://ui-avatars.com/api/?name={initials}&size=200&background=8B5CF6&color=fff"
    
    return ProfileFullOut(
        user_id=user.id,
        username=user.username,
        email=user.email,
        first_name=profile.first_name,
        last_name=profile.last_name,
        avatar_url=avatar_url,
        level=profile.level,
        coins=profile.coins or 0,
        streak=profile.streak or 0,
        rating_points=profile.rating_points or 0,
        completed_modules=completed_modules,
        total_modules=total_modules,
        achievements_count=achievements_count,
        progress_percent=progress_percent
    )