from pydantic import BaseModel
from typing import Optional
from datetime import date


class ProfileOut(BaseModel):
    user_id: int
    bio: Optional[str]
    coins: int
    streak: int
    last_active: Optional[date]
    rating_points: int
    class Config:
        from_attributes = True