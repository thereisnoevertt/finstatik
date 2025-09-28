from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from app.db.session import get_session
from app.models.lesson import Lesson
from app.models.profile import Profile
from app.models.user import User
from app.schemas.lesson import LessonOut
from app.core.security import decode_token
from fastapi import Header
from datetime import date, timedelta

router = APIRouter(prefix="/lessons", tags=["lessons"])

async def get_current_user(token: str = Header(None), session: AsyncSession = Depends(get_session)):
    if not token:
        raise HTTPException(status_code=401, detail="Missing token header")
    payload = decode_token(token.replace("Bearer ", ""))
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = await session.get(User, int(payload.get("sub")))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.get("/{lesson_id}", response_model=LessonOut)
async def get_lesson(lesson_id: int, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    lesson = await session.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # check prerequisite
    if lesson.prerequisite_id:
        result = await session.execute(
            text("SELECT 1 FROM user_lessons WHERE user_id = :uid AND lesson_id = :lid"),
            {"uid": user.id, "lid": lesson.prerequisite_id}
        )
        if result.first() is None:
            raise HTTPException(status_code=403, detail="Lesson locked. Complete prerequisite first.")
    return lesson

@router.post("/{lesson_id}/complete")
async def complete_content_lesson(lesson_id: int, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    lesson = await session.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    if lesson.is_quiz:
        raise HTTPException(status_code=400, detail="This is a quiz lesson, not a content lesson")
    
    # check already completed
    result = await session.execute(
        text("SELECT 1 FROM user_lessons WHERE user_id = :uid AND lesson_id = :lid"),
        {"uid": user.id, "lid": lesson.id}
    )
    if result.first():
        raise HTTPException(status_code=400, detail="Lesson already completed")
    
    # mark completed
    await session.execute(
        text("INSERT INTO user_lessons (user_id, lesson_id, completed_at) VALUES (:uid, :lid, now())"),
        {"uid": user.id, "lid": lesson.id}
    )
    
    profile = await session.get(Profile, user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
        
    profile.coins = (profile.coins or 0) + (lesson.reward_coins or 0)
    today = date.today()
    
    if profile.last_active == today:
        pass
    else:
        if profile.last_active and (profile.last_active == today - timedelta(days=1)):
            profile.streak = (profile.streak or 0) + 1
        else:
            profile.streak = 1
        profile.last_active = today
    
    profile.rating_points = (profile.rating_points or 0) + max(1, (lesson.reward_coins or 0) // 10)
    await session.commit()
    
    return {"ok": True, "awarded_coins": lesson.reward_coins, "new_balance": profile.coins}