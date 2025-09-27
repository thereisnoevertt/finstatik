from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.lesson import Lesson
from app.models.quiz import QuizQuestion


async def get_lesson(session: AsyncSession, lesson_id: int):
    return await session.get(Lesson, lesson_id)


async def get_modules(session: AsyncSession):
    q = select(Lesson).order_by(Lesson.sort_order)
    # we'll fetch modules in router by relationship
    return


async def get_quiz_questions(session: AsyncSession, lesson_id: int):
    q = select(QuizQuestion).where(QuizQuestion.lesson_id == lesson_id)
    r = await session.execute(q)
    return r.scalars().all()