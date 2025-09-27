from pydantic import BaseModel
from typing import Optional, Dict


class LessonOut(BaseModel):
    id: int
    module_id: int
    title: str
    type: str
    reward_coins: int
    duration_seconds: int
    content: Optional[Dict]
    prerequisite_id: Optional[int]
    class Config:
        orm_mode = True