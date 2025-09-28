from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, func
from app.db.base import Base

class UserLesson(Base):
    __tablename__ = "user_lessons"
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), primary_key=True)
    completed_at = Column(TIMESTAMP(timezone=True), server_default=func.now())