from pydantic import BaseModel
from typing import List


class QuizQuestionOut(BaseModel):
    id: int
    question: str
    options: List[str]
    class Config:
        orm_mode = True


class QuizSubmit(BaseModel):
    answers: List[int]


class QuizResult(BaseModel):
    score: int
    passed: bool
    awarded_coins: int
    new_balance: int
    unlocked_lessons: List[int] = []