from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True, index=True)  # @elena1979
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)  # БЕЗ хеширования
    avatar_url = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=func.now)
    
    profile = relationship("Profile", uselist=False, back_populates="user")
    goals = relationship("Goal", back_populates="user")