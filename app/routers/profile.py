from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.schemas.profile import ProfileOut
from app.db.session import get_session
from app.core.security import decode_token
from fastapi import Header, HTTPException
from app.models.profile import Profile
from app.models.user import User


router = APIRouter(prefix="/profile", tags=["profile"])


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


@router.get("/me", response_model=ProfileOut)
async def me(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    profile = await session.get(Profile, user.id)
    return profile