from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.schemas.user import UserCreate, UserOut, UserLogin
from app.crud.user import get_user_by_email, get_user_by_username, create_user
from app.core.security import verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

# Простое хранилище сессий в памяти (для production использовать Redis)
active_sessions = {}

@router.post("/register", response_model=UserOut)
async def register(payload: UserCreate, session: AsyncSession = Depends(get_session)):
    """Регистрация нового пользователя"""
    
    # Проверка существующего username
    existing = await get_user_by_username(payload.username, session)
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Проверка существующего email
    existing_email = await get_user_by_email(payload.email, session)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Создание пользователя
    user = await create_user(
        payload.username,
        payload.email,
        payload.first_name,
        payload.last_name,
        payload.password,
        session
    )
    return user

@router.post("/login")
async def login(
    payload: UserLogin, 
    response: Response,
    session: AsyncSession = Depends(get_session)
):
    """Вход в систему (простая сессия)"""
    
    # Попробовать найти по username или email
    user = await get_user_by_username(payload.username, session)
    if not user:
        user = await get_user_by_email(payload.username, session)
    
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # Создать простую сессию
    session_id = f"session_{user.id}"
    active_sessions[session_id] = user.id
    
    # Установить cookie
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    
    return {
        "message": "Login successful",
        "user_id": user.id,
        "username": user.username
    }

@router.post("/logout")
async def logout(response: Response, request: Request):
    """Выход из системы"""
    session_id = request.cookies.get("session_id")
    if session_id and session_id in active_sessions:
        del active_sessions[session_id]
    response.delete_cookie("session_id")
    return {"message": "Logout successful"}