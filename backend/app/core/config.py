from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Telusko Workflow Engine"
    database_url: str = "sqlite+aiosqlite:///./telusko.db"
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    port: int = 8000

    class Config:
        env_file = ".env"


settings = Settings()
