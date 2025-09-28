from fastapi import FastAPI
from app.routers import auth, profile, modules, lessons, quiz, store, goals, leaderboard, achievements
from app.db.base import Base
from app.db.session import engine


app = FastAPI(title="Fintastic API")


app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(modules.router)
app.include_router(lessons.router)
app.include_router(quiz.router)
app.include_router(store.router)
app.include_router(goals.router)
app.include_router(achievements.router)
app.include_router(leaderboard.router)


@app.on_event("startup")
async def startup():
# dev helper: create tables if not exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)