# app/schemas/lesson.py
from pydantic import BaseModel

class LessonBase(BaseModel):
    title: str
    content: str | None = None
    is_quiz: bool

class LessonOut(LessonBase):
    id: int
    prerequisite_id: int | None

    class Config:
        orm_mode = True

class ModuleOut(BaseModel):
    id: int
    title: str
    description: str | None
    lessons: list[LessonOut] = []

    class Config:
        orm_mode = True
