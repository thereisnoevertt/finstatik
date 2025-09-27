from sqlalchemy import Column, BigInteger, String, Integer, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from app.db.base import Base


class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(BigInteger, primary_key=True)
    module_id = Column(BigInteger, ForeignKey("modules.id", ondelete="CASCADE"))
    title = Column(String, nullable=False)
    content = Column(JSON, nullable=True) # for content lessons
    type = Column(String, default="content") # content | quiz
    prerequisite_id = Column(BigInteger, ForeignKey("lessons.id"), nullable=True)
    reward_coins = Column(Integer, default=10)
    duration_seconds = Column(Integer, default=300)
    sort_order = Column(Integer, default=0)


    module = relationship("Module", back_populates="lessons")
    quiz_questions = relationship("QuizQuestion", back_populates="lesson")