from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.models.user import User
from app.routers.auth import active_sessions

async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_session)
) -> User:
    """Получить текущего пользователя из сессии"""
    session_id = request.cookies.get("session_id")
    
    if not session_id or session_id not in active_sessions:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user_id = active_sessions[session_id]
    user = await session.get(User, user_id)
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

async def get_current_user_optional(
    request: Request,
    session: AsyncSession = Depends(get_session)
) -> User | None:
    """Получить текущего пользователя (опционально)"""
    session_id = request.cookies.get("session_id")
    
    if not session_id or session_id not in active_sessions:
        return None
    
    user_id = active_sessions.get(session_id)
    if not user_id:
        return None
        
    user = await session.get(User, user_id)
    return user
