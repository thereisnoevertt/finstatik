from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from app.db import Base

class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)

    lessons = relationship("Lesson", back_populates="module")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"))
    title = Column(String, nullable=False)
    content = Column(Text)               # текст теоретического урока
    is_quiz = Column(Boolean, default=False)
    prerequisite_id = Column(Integer, ForeignKey("lessons.id"), nullable=True)

    module = relationship("Module", back_populates="lessons")
    prerequisite = relationship("Lesson", remote_side=[id])
