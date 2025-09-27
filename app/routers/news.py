from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app import models, schemas

router = APIRouter(prefix="/news", tags=["news"])

@router.get("/", response_model=list[schemas.NewsOut])
def get_news(db: Session = Depends(get_db)):
    return db.query(models.News).order_by(models.News.created_at.desc()).all()

@router.post("/", response_model=schemas.NewsOut)
def create_news(news: schemas.NewsCreate, db: Session = Depends(get_db)):
    item = models.News(**news.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
