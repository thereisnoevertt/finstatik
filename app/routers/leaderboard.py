from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.session import get_session
from app.core.security import decode_token
from app.models.user import User
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


class LeaderboardEntry(BaseModel):
    """Запись в лидерборде"""
    position: int
    user_id: int
    display_name: str
    avatar_url: Optional[str]
    rating_points: int
    coins: int
    streak: int
    is_current_user: bool = False
    
    class Config:
        from_attributes = True


class LeaderboardResponse(BaseModel):
    """Ответ с лидербордом"""
    leaderboard: List[LeaderboardEntry]
    current_user_position: Optional[int] = None
    total_users: int


async def get_current_user_optional(token: str = Header(None), session: AsyncSession = Depends(get_session)):
    """Получение текущего пользователя (опционально)"""
    if not token:
        return None
    try:
        payload = decode_token(token.replace("Bearer ", ""))
        if not payload:
            return None
        user = await session.get(User, int(payload.get("sub")))
        return user
    except:
        return None


def generate_avatar_url(display_name: str, avatar_url: Optional[str]) -> str:
    """Генерация URL аватара"""
    if avatar_url:
        return avatar_url
    # Генерация инициалов
    initials = ''.join([word[0].upper() for word in display_name.split()[:2]])
    return f"https://ui-avatars.com/api/?name={initials}&size=200&background=8B5CF6&color=fff"


@router.get("/rating", response_model=LeaderboardResponse)
async def get_rating_leaderboard(
    limit: int = 50,
    user: Optional[User] = Depends(get_current_user_optional),
    session: AsyncSession = Depends(get_session)
):
    """Лидерборд по рейтинговым очкам"""
    
    # Получение топа пользователей
    stmt = text("""
        SELECT 
            ROW_NUMBER() OVER (ORDER BY p.rating_points DESC, p.coins DESC) AS position,
            p.user_id, 
            u.display_name,
            u.avatar_url,
            p.rating_points, 
            p.coins, 
            p.streak
        FROM profiles p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.rating_points DESC, p.coins DESC
        LIMIT :limit
    """)
    result = await session.execute(stmt, {"limit": limit})
    rows = result.fetchall()
    
    # Получение общего количества пользователей
    total_stmt = text("SELECT COUNT(*) FROM profiles")
    total_result = await session.execute(total_stmt)
    total_users = total_result.scalar()
    
    # Формирование записей лидерборда
    leaderboard = []
    current_user_position = None
    
    for row in rows:
        position, user_id, display_name, avatar_url, rating_points, coins, streak = row
        
        is_current = user and user.id == user_id
        if is_current:
            current_user_position = position
        
        leaderboard.append(LeaderboardEntry(
            position=position,
            user_id=user_id,
            display_name=display_name,
            avatar_url=generate_avatar_url(display_name, avatar_url),
            rating_points=rating_points,
            coins=coins,
            streak=streak,
            is_current_user=is_current
        ))
    
    # Если текущий пользователь не в топе, найти его позицию
    if user and current_user_position is None:
        position_stmt = text("""
            SELECT position FROM (
                SELECT 
                    user_id,
                    ROW_NUMBER() OVER (ORDER BY rating_points DESC, coins DESC) AS position
                FROM profiles
            ) ranked
            WHERE user_id = :uid
        """)
        position_result = await session.execute(position_stmt, {"uid": user.id})
        position_row = position_result.fetchone()
        if position_row:
            current_user_position = position_row[0]
    
    return LeaderboardResponse(
        leaderboard=leaderboard,
        current_user_position=current_user_position,
        total_users=total_users
    )


@router.get("/coins", response_model=LeaderboardResponse)
async def get_coins_leaderboard(
    limit: int = 50,
    user: Optional[User] = Depends(get_current_user_optional),
    session: AsyncSession = Depends(get_session)
):
    """Лидерборд по монетам"""
    
    stmt = text("""
        SELECT 
            ROW_NUMBER() OVER (ORDER BY p.coins DESC, p.rating_points DESC) AS position,
            p.user_id, 
            u.display_name,
            u.avatar_url,
            p.rating_points, 
            p.coins, 
            p.streak
        FROM profiles p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.coins DESC, p.rating_points DESC
        LIMIT :limit
    """)
    result = await session.execute(stmt, {"limit": limit})
    rows = result.fetchall()
    
    total_stmt = text("SELECT COUNT(*) FROM profiles")
    total_result = await session.execute(total_stmt)
    total_users = total_result.scalar()
    
    leaderboard = []
    current_user_position = None
    
    for row in rows:
        position, user_id, display_name, avatar_url, rating_points, coins, streak = row
        
        is_current = user and user.id == user_id
        if is_current:
            current_user_position = position
        
        leaderboard.append(LeaderboardEntry(
            position=position,
            user_id=user_id,
            display_name=display_name,
            avatar_url=generate_avatar_url(display_name, avatar_url),
            rating_points=rating_points,
            coins=coins,
            streak=streak,
            is_current_user=is_current
        ))
    
    if user and current_user_position is None:
        position_stmt = text("""
            SELECT position FROM (
                SELECT 
                    user_id,
                    ROW_NUMBER() OVER (ORDER BY coins DESC, rating_points DESC) AS position
                FROM profiles
            ) ranked
            WHERE user_id = :uid
        """)
        position_result = await session.execute(position_stmt, {"uid": user.id})
        position_row = position_result.fetchone()
        if position_row:
            current_user_position = position_row[0]
    
    return LeaderboardResponse(
        leaderboard=leaderboard,
        current_user_position=current_user_position,
        total_users=total_users
    )


@router.get("/streak", response_model=LeaderboardResponse)
async def get_streak_leaderboard(
    limit: int = 50,
    user: Optional[User] = Depends(get_current_user_optional),
    session: AsyncSession = Depends(get_session)
):
    """Лидерборд по серии дней подряд"""
    
    stmt = text("""
        SELECT 
            ROW_NUMBER() OVER (ORDER BY p.streak DESC, p.rating_points DESC) AS position,
            p.user_id, 
            u.display_name,
            u.avatar_url,
            p.rating_points, 
            p.coins, 
            p.streak
        FROM profiles p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.streak DESC, p.rating_points DESC
        LIMIT :limit
    """)
    result = await session.execute(stmt, {"limit": limit})
    rows = result.fetchall()
    
    total_stmt = text("SELECT COUNT(*) FROM profiles")
    total_result = await session.execute(total_stmt)
    total_users = total_result.scalar()
    
    leaderboard = []
    current_user_position = None
    
    for row in rows:
        position, user_id, display_name, avatar_url, rating_points, coins, streak = row
        
        is_current = user and user.id == user_id
        if is_current:
            current_user_position = position
        
        leaderboard.append(LeaderboardEntry(
            position=position,
            user_id=user_id,
            display_name=display_name,
            avatar_url=generate_avatar_url(display_name, avatar_url),
            rating_points=rating_points,
            coins=coins,
            streak=streak,
            is_current_user=is_current
        ))
    
    if user and current_user_position is None:
        position_stmt = text("""
            SELECT position FROM (
                SELECT 
                    user_id,
                    ROW_NUMBER() OVER (ORDER BY streak DESC, rating_points DESC) AS position
                FROM profiles
            ) ranked
            WHERE user_id = :uid
        """)
        position_result = await session.execute(position_stmt, {"uid": user.id})
        position_row = position_result.fetchone()
        if position_row:
            current_user_position = position_row[0]
    
    return LeaderboardResponse(
        leaderboard=leaderboard,
        current_user_position=current_user_position,
        total_users=total_users
    )