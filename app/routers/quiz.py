from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from app.db.session import get_session
from app.models.lesson import Lesson
from app.models.quiz import QuizQuestion, UserQuizAttempt
from app.models.profile import Profile
from app.models.user import User
from app.core.security import decode_token
from fastapi import Header
from app.schemas.quiz import QuizQuestionOut, QuizSubmit, QuizResult

router = APIRouter(prefix="/quiz", tags=["quiz"])  # Изменен префикс

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

@router.get("/{lesson_id}", response_model=list[QuizQuestionOut])
async def get_quiz(lesson_id: int, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    lesson = await session.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    if not lesson.is_quiz:
        raise HTTPException(status_code=400, detail="This lesson is not a quiz")
    
    # check prerequisite
    if lesson.prerequisite_id:
        result = await session.execute(
            text("SELECT 1 FROM user_lessons WHERE user_id = :uid AND lesson_id = :lid"),
            {"uid": user.id, "lid": lesson.prerequisite_id}
        )
        if result.first() is None:
            raise HTTPException(status_code=403, detail="Lesson locked. Complete prerequisite first.")
    
    stmt = select(QuizQuestion).where(QuizQuestion.lesson_id == lesson_id)
    result = await session.execute(stmt)
    questions = result.scalars().all()
    
    return [QuizQuestionOut(id=q.id, question=q.question, options=q.options) for q in questions]

@router.post("/{lesson_id}/submit", response_model=QuizResult)
async def submit_quiz(lesson_id: int, payload: QuizSubmit, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    lesson = await session.get(Lesson, lesson_id)
    if not lesson or not lesson.is_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    stmt = select(QuizQuestion).where(QuizQuestion.lesson_id == lesson_id).order_by(QuizQuestion.id)
    result = await session.execute(stmt)
    questions = result.scalars().all()
    
    if len(payload.answers) != len(questions):
        raise HTTPException(status_code=400, detail="Answers count mismatch")
    
    correct = 0
    for ans, q in zip(payload.answers, questions):
        if ans == q.correct_option:
            correct += 1
    
    score = int((correct / len(questions)) * 100)
    passed = score >= 70
    
    # record attempt
    attempt = UserQuizAttempt(
        user_id=user.id, 
        lesson_id=lesson_id, 
        score=score, 
        passed=passed
    )
    session.add(attempt)
    
    awarded = 0
    unlocked = []
    profile = await session.get(Profile, user.id)
    
    if passed:
        # mark completed
        await session.execute(
            text("INSERT INTO user_lessons (user_id, lesson_id, completed_at) VALUES (:uid, :lid, now()) ON CONFLICT DO NOTHING"),
            {"uid": user.id, "lid": lesson.id}
        )
        awarded = lesson.reward_coins or 0
        profile.coins = (profile.coins or 0) + awarded
        profile.rating_points = (profile.rating_points or 0) + max(1, awarded // 10)
        
        # try to unlock next lessons
        result = await session.execute(
            text("SELECT id FROM lessons WHERE prerequisite_id = :lid"), 
            {"lid": lesson.id}
        )
        unlocked = [row[0] for row in result.fetchall()]
    
    await session.commit()
    return QuizResult(
        score=score, 
        passed=passed, 
        awarded_coins=awarded, 
        new_balance=profile.coins or 0, 
        unlocked_lessons=unlocked
    )