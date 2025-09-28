import os


class Settings:
    PROJECT_NAME: str = "Finstatic"
    DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://fintastic:fintastic_pass@localhost:5432/fintastic_db"
    )
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-prod")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    ALGORITHM: str = "HS256"


settings = Settings()