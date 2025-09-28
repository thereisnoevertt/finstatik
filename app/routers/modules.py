from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.models.module import Module
from app.schemas.module import ModuleOut
from sqlalchemy.orm import Session
from app.db import get_db
from app import models, schemas

router = APIRouter(prefix="/modules", tags=["modules"])


@router.get("/", response_model=list[ModuleOut])
async def list_modules(session: AsyncSession = Depends(get_session)):
    res = await session.execute(Module.__table__.select().order_by(Module.sort_order))
    modules = res.scalars().all()
    # eager load lessons
    for m in modules:
        await session.refresh(m, attribute_names=["lessons"])
    return modules

@router.get("/", response_model=list[schemas.ModuleOut])
def get_modules(db: Session = Depends(get_db)):
    return db.query(models.Module).all()