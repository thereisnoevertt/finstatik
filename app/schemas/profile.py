from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProfileOut(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    coins: int
    streak: int
    last_active: Optional[date]
    rating_points: int
    level: str
    
    class Config:
        from_attributes = True

class ProfileFullOut(BaseModel):
    """Полная информация профиля для страницы профиля"""
    user_id: int
    username: str
    email: str
    first_name: str
    last_name: str
    avatar_url: Optional[str]
    level: str
    coins: int
    streak: int
    rating_points: int
    
    # Статистика
    completed_modules: int
    total_modules: int
    achievements_count: int
    progress_percent: int
    
    class Config:
        from_attributes = True

class AchievementOut(BaseModel):
    """Достижение для отображения"""
    id: str
    title: str
    description: str
    icon: str
    is_unlocked: bool
    progress: int