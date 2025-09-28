from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"))
    title = Column(String, nullable=False)
    content = Column(Text)
    is_quiz = Column(Boolean, default=False)
    prerequisite_id = Column(Integer, ForeignKey("lessons.id"), nullable=True)
    sort_order = Column(Integer, default=0)
    reward_coins = Column(Integer, default=10)  # Добавлено поле для наград

    module = relationship("Module", back_populates="lessons")
    prerequisite = relationship("Lesson", remote_side=[id])
    quiz_questions = relationship("QuizQuestion", back_populates="lesson")