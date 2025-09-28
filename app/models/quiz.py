from sqlalchemy import Column, Integer, ForeignKey, Text, JSON, Boolean, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.db.base import Base


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"))
    question = Column(Text, nullable=False)
    options = Column(JSON, nullable=False) # list of options
    correct_option = Column(Integer, nullable=False)
    lesson = relationship("Lesson", back_populates="quiz_questions")


class UserQuizAttempt(Base):
    __tablename__ = "user_quiz_attempts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"))
    score = Column(Integer, nullable=False)
    passed = Column(Boolean, nullable=False)
    attempted_at = Column(TIMESTAMP(timezone=True), server_default=func.now())