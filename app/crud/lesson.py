from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.lesson import Lesson
from app.models.quiz import QuizQuestion
from app.models.module import Module

async def get_lesson(session: AsyncSession, lesson_id: int):
    return await session.get(Lesson, lesson_id)

async def get_modules_with_lessons(session: AsyncSession):
    """Получить все модули с уроками"""
    stmt = select(Module).options(selectinload(Module.lessons)).order_by(Module.sort_order)
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_quiz_questions(session: AsyncSession, lesson_id: int):
    stmt = select(QuizQuestion).where(QuizQuestion.lesson_id == lesson_id)
    result = await session.execute(stmt)
    return result.scalars().all()

async def is_lesson_completed(session: AsyncSession, user_id: int, lesson_id: int) -> bool:
    """Проверить, завершен ли урок пользователем"""
    result = await session.execute(
        text("SELECT 1 FROM user_lessons WHERE user_id = :uid AND lesson_id = :lid"),
        {"uid": user_id, "lid": lesson_id}
    )
    return result.first() is not None

async def complete_lesson(session: AsyncSession, user_id: int, lesson_id: int):
    """Отметить урок как завершенный"""
    await session.execute(
        text("INSERT INTO user_lessons (user_id, lesson_id, completed_at) VALUES (:uid, :lid, now()) ON CONFLICT DO NOTHING"),
        {"uid": user_id, "lid": lesson_id}
    )