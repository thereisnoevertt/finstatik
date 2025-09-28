from pydantic import BaseModel
from typing import Optional

class LessonBase(BaseModel):
    title: str
    content: Optional[str] = None
    is_quiz: bool

class LessonOut(LessonBase):
    id: int
    module_id: int
    prerequisite_id: Optional[int]
    sort_order: int
    reward_coins: int

    class Config:
        from_attributes = True  # Обновлено для Pydantic v2