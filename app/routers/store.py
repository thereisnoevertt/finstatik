from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.models.store import StoreItem, Purchase
from app.models.profile import Profile
from app.models.user import User
from app.core.security import decode_token
from fastapi import Header


router = APIRouter(prefix="/store", tags=["store"])


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


@router.get("/", response_model=list[dict])
async def list_store(session: AsyncSession = Depends(get_session)):
    res = await session.execute(StoreItem.__table__.select().order_by(StoreItem.id))
    return res.scalars().all()


@router.post("/buy/{item_id}")
async def buy(item_id: int, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    item = await session.get(StoreItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    profile = await session.get(Profile, user.id)
    if (profile.coins or 0) < item.price_coins:
        raise HTTPException(status_code=400, detail="Not enough coins")
    profile.coins = profile.coins - item.price_coins
    await session.execute(Purchase.__table__.insert().values(user_id=user.id, item_id=item.id))
    await session.commit()
    return {"ok": True, "new_balance": profile.coins}