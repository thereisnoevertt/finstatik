from fastapi import FastAPI
from app.routers import auth, profile, modules, lessons, quiz, store, goals, leaderboard, news
from app.db.session import engine
from app.db.base import Base

app = FastAPI(title="Finstatik API")

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
    # Импортировать через отдельные импорты без конфликтов
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