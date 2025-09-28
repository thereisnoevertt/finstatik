from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.session import get_session
from app.models.module import Module
from app.schemas.module import ModuleOut

router = APIRouter(prefix="/modules", tags=["modules"])

@router.get("/", response_model=list[ModuleOut])
async def list_modules(session: AsyncSession = Depends(get_session)):
    # Используем selectinload для eager loading
    stmt = select(Module).options(selectinload(Module.lessons)).order_by(Module.sort_order)
    result = await session.execute(stmt)
    modules = result.scalars().all()
    return modules