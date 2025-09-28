from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.models.lesson import Lesson
from app.schemas.lesson import LessonOut
from app.models.profile import Profile
from app.models.user import User
from app.core.security import decode_token
from fastapi import Header
from datetime import date
from sqlalchemy.orm import Session
from app.db import get_db
from app import models, schemas



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
    # check if user completed prerequisite
        q = await session.execute(
            "SELECT 1 FROM user_lessons WHERE user_id = :uid AND lesson_id = :lid",
            {"uid": user.id, "lid": lesson.prerequisite_id}
        )
        if q.first() is None:
            # locked
            raise HTTPException(status_code=403, detail="Lesson locked. Complete prerequisite first.")
    return lesson


@router.post("/{lesson_id}/complete")
async def complete_content_lesson(lesson_id: int, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    lesson = await session.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    if lesson.type != "content":
        raise HTTPException(status_code=400, detail="Not a content lesson")
    # check already completed
    q = await session.execute(
    "SELECT 1 FROM user_lessons WHERE user_id = :uid AND lesson_id = :lid",
    {"uid": user.id, "lid": lesson.id}
    )
    if q.first():
        raise HTTPException(status_code=400, detail="Lesson already completed")
    # mark completed
    await session.execute(
    "INSERT INTO user_lessons (user_id, lesson_id, completed_at) VALUES (:uid, :lid, now())",
    {"uid": user.id, "lid": lesson.id}
    )
    profile = await session.get(Profile, user.id)
    profile.coins = (profile.coins or 0) + (lesson.reward_coins or 0)
    today = date.today()
    if profile.last_active == today:
        pass
    else:
        if profile.last_active and (profile.last_active.toordinal() == today.toordinal() - 1):
            profile.streak = (profile.streak or 0) + 1
        else:
            profile.streak = 1
        profile.last_active = today
    profile.rating_points = (profile.rating_points or 0) + max(1, (lesson.reward_coins or 0) // 10)
    await session.commit()
    return {"ok": True, "awarded_coins": lesson.reward_coins, "new_balance": profile.coins}

@router.get("/{lesson_id}", response_model=schemas.LessonOut)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(404, "Lesson not found")
    return lesson


@router.get("/{lesson_id}/quiz")
def get_quiz_questions(lesson_id: int, db: Session = Depends(get_db)):
    questions = db.query(models.QuizQuestion).filter(
        models.QuizQuestion.lesson_id == lesson_id
    ).all()
    return questions


@router.post("/{lesson_id}/submit")
def submit_quiz(lesson_id: int, answers: dict, db: Session = Depends(get_db)):
    # TODO: проверить ответы, сохранить UserQuizAttempt
    return {"status": "ok", "score": 10}
