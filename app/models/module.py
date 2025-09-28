from sqlalchemy import Column, Integer, String, Text, Integer
from sqlalchemy.orm import relationship
from app.db.base import Base


class Module(Base):
    __tablename__ = "modules"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    sort_order = Column(Integer, default=0)
    lessons = relationship("Lesson", back_populates="module", order_by="Lesson.sort_order")