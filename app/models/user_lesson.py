from sqlalchemy import Column, BigInteger, ForeignKey, TIMESTAMP, func
from app.db.base import Base

class UserLesson(Base):
    __tablename__ = "user_lessons"
    
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    lesson_id = Column(BigInteger, ForeignKey("lessons.id", ondelete="CASCADE"), primary_key=True)
    completed_at = Column(TIMESTAMP(timezone=True), server_default=func.now())