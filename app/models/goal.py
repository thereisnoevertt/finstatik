from sqlalchemy import Column, BigInteger, String, Integer, ForeignKey, TIMESTAMP, func
from app.db.base import Base


class Goal(Base):
    __tablename__ = "goals"
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    title = Column(String, nullable=False)
    target_amount = Column(Integer, nullable=False)
    current_amount = Column(Integer, default=0)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())