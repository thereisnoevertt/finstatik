from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.session import get_session
from pydantic import BaseModel

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])

class LeaderboardEntry(BaseModel):
    user_id: int
    display_name: str
    rating_points: int
    coins: int
    streak: int
    
    class Config:
        from_attributes = True

@router.get("/rating", response_model=list[LeaderboardEntry])
async def get_rating_leaderboard(limit: int = 50, session: AsyncSession = Depends(get_session)):
    """Лидерборд по рейтинговым очкам"""
    stmt = text("""
        SELECT p.user_id, u.display_name, p.rating_points, p.coins, p.streak
        FROM profiles p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.rating_points DESC
        LIMIT :limit
    """)
    result = await session.execute(stmt, {"limit": limit})
    rows = result.fetchall()
    return [
        LeaderboardEntry(
            user_id=row[0],
            display_name=row[1], 
            rating_points=row[2],
            coins=row[3],
            streak=row[4]
        ) for row in rows
    ]

@router.get("/coins", response_model=list[LeaderboardEntry])
async def get_coins_leaderboard(limit: int = 50, session: AsyncSession = Depends(get_session)):
    """Лидерборд по монетам"""
    stmt = text("""
        SELECT p.user_id, u.display_name, p.rating_points, p.coins, p.streak
        FROM profiles p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.coins DESC
        LIMIT :limit
    """)
    result = await session.execute(stmt, {"limit": limit})
    rows = result.fetchall()
    return [
        LeaderboardEntry(
            user_id=row[0],
            display_name=row[1], 
            rating_points=row[2],
            coins=row[3],
            streak=row[4]
        ) for row in rows
    ]

@router.get("/streak", response_model=list[LeaderboardEntry])
async def get_streak_leaderboard(limit: int = 50, session: AsyncSession = Depends(get_session)):
    """Лидерборд по серии дней подряд"""
    stmt = text("""
        SELECT p.user_id, u.display_name, p.rating_points, p.coins, p.streak
        FROM profiles p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.streak DESC
        LIMIT :limit
    """)
    result = await session.execute(stmt, {"limit": limit})
    rows = result.fetchall()
    return [
        LeaderboardEntry(
            user_id=row[0],
            display_name=row[1], 
            rating_points=row[2],
            coins=row[3],
            streak=row[4]
        ) for row in rows
    ]