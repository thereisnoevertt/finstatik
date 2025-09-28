from pydantic import BaseModel
from typing import Optional


class StoreItemOut(BaseModel):
    id: int
    key: str
    title: str
    price_coins: int
    item_metadata: Optional[dict]
    class Config:
        from_attributes = True