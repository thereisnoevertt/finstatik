from sqlalchemy import Column, Integer, ForeignKey, Text, Integer, Date
from sqlalchemy.orm import relationship
from app.db.base import Base


class Profile(Base):
    __tablename__ = "profiles"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    bio = Column(Text, nullable=True)
    coins = Column(Integer, default=0)
    streak = Column(Integer, default=0)
    last_active = Column(Date, nullable=True)
    rating_points = Column(Integer, default=0)
    user = relationship("User", back_populates="profile")