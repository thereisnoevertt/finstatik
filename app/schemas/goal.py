from pydantic import BaseModel
from datetime import datetime

class GoalBase(BaseModel):
    title: str
    target_amount: int

class GoalCreate(GoalBase):
    pass

class GoalOut(GoalBase):
    id: int
    current_amount: int
    created_at: datetime

    class Config:
        from_attributes = True