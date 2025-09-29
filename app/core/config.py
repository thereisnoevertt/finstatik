import os

class Settings:
    PROJECT_NAME: str = "Finstatic"
    # SQLite база данных
    DATABASE_URL: str = "sqlite+aiosqlite:///./finstatik.db"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-prod")

settings = Settings()