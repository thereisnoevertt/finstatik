from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, profile, modules, lessons, quiz, store, goals, leaderboard, news
from app.db.session import engine
from app.db.base import Base
import os

app = FastAPI(title="Finstatik API")

# CORS для локальной разработки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создание директории для аватаров
os.makedirs("uploads/avatars", exist_ok=True)

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(modules.router)
app.include_router(lessons.router)
app.include_router(quiz.router)
app.include_router(store.router)
app.include_router(goals.router)
app.include_router(news.router)
app.include_router(leaderboard.router)

@app.on_event("startup")
async def startup():
    """Создание таблиц при запуске"""
    import app.models.user
    import app.models.profile
    import app.models.module
    import app.models.lesson
    import app.models.quiz
    import app.models.goal
    import app.models.store
    import app.models.news
    import app.models.user_lesson
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Database tables created successfully")
    print("📊 SQLite database: finstatik.db")
    print("🚀 Server running on http://localhost:8000")
    print("📚 Swagger docs: http://localhost:8000/docs")

@app.get("/")
async def root():
    return {
        "message": "Finstatik API",
        "docs": "/docs",
        "database": "SQLite"
    }