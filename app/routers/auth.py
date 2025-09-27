from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.schemas.user import UserCreate, UserOut
from app.crud.user import get_user_by_email, create_user
from app.core.security import verify_password, create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
async def register(payload: UserCreate, session: AsyncSession = Depends(get_session)):
    existing = await get_user_by_email(payload.email, session)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await create_user(payload.email, payload.display_name, payload.password, session)
    return user


@router.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    user = await get_user_by_email(form_data.username, session)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token(str(user.id))
    return {"access_token": token, "token_type": "bearer"}