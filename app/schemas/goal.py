from pydantic import BaseModel


class GoalCreate(BaseModel):
    title: str
    target_amount: int


class GoalOut(BaseModel):
    id: int
    title: str
    target_amount: int
    current_amount: int
    class Config:
        orm_mode = True