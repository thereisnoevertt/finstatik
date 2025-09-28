from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_session
from app.models.news import News
from app.schemas.news import NewsOut, NewsCreate

router = APIRouter(prefix="/news", tags=["news"])

@router.get("/", response_model=list[NewsOut])
async def get_news(session: AsyncSession = Depends(get_session)):
    stmt = select(News).order_by(News.created_at.desc())
    result = await session.execute(stmt)
    return result.scalars().all()

@router.post("/", response_model=NewsOut)
async def create_news(news: NewsCreate, session: AsyncSession = Depends(get_session)):
    item = News(**news.dict())
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item