from sqlalchemy import Column, BigInteger, String, Integer, JSON, ForeignKey, TIMESTAMP, func
from app.db.base import Base


class StoreItem(Base):
    __tablename__ = "store_items"
    id = Column(BigInteger, primary_key=True)
    key = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    price_coins = Column(Integer, nullable=False)
    metadata = Column(JSON)


class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    item_id = Column(BigInteger, ForeignKey("store_items.id", ondelete="RESTRICT"))
    purchased_at = Column(TIMESTAMP(timezone=True), server_default=func.now())