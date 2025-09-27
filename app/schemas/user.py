from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    display_name: str
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    display_name: str
    class Config:
        orm_mode = True