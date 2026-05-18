from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Technogym FastAPI Backend"
    ENV: str = "development"
    HOST: str = "0.0.0.0"
    PORT: int = 5000
    FRONTEND_URL: str = "http://localhost:5173"
    DATABASE_URL: str = "sqlite:///./data/technogym.db"
    MONGODB_URI: str = ""
    MONGODB_DB_NAME: str = "technogym_redesign"

    class Config:
        env_file = ".env"


settings = Settings()
