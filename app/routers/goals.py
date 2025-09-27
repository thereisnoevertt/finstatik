from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.models.goal import Goal
from app.models.profile import Profile
from app.models.user import User
from app.core.security import decode_token
from fastapi import Header
from app.schemas.goal import GoalCreate, GoalOut


router = APIRouter(prefix="/goals", tags=["goals"])


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


@router.post("/", response_model=GoalOut)
async def create_goal(payload: GoalCreate, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    g = Goal(user_id=user.id, title=payload.title, target_amount=payload.target_amount)
    session.add(g)
    await session.commit()
    await session.refresh(g)
    return g


@router.get("/", response_model=list[GoalOut])
async def list_goals(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    res = await session.execute(Goal.__table__.select().where(Goal.user_id == user.id))
    return res.scalars().all()


@router.post("/{goal_id}/deposit")
async def deposit(goal_id: int, amount: int, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    goal = await session.get(Goal, goal_id)
    if not goal or goal.user_id != user.id:
        raise HTTPException(status_code=404, detail="Goal not found")
    profile = await session.get(Profile, user.id)
    if (profile.coins or 0) < amount:
        raise HTTPException(status_code=400, detail="Not enough coins")
    profile.coins = profile.coins - amount
    goal.current_amount = (goal.current_amount or 0) + amount
    await session.commit()
    return {"ok": True, "goal": goal.current_amount}