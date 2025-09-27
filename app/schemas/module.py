from pydantic import BaseModel
from typing import List, Optional
from app.schemas.lesson import LessonOut


class ModuleOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    lessons: List[LessonOut] = []
    class Config:
        orm_mode = True