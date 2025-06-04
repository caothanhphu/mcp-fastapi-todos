from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Cấu hình ứng dụng"""
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"
    
    # CORS
    # ALLOWED_ORIGINS: List[str] = [
    #     "http://localhost:3000",  # React development server
    #     "http://localhost:5173",  # Vite development server
    #     "http://127.0.0.1:3000",
    #     "http://127.0.0.1:5173",
    # ]
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # App
    DEBUG: bool = True
    APP_NAME: str = "FastAPI Backend"
    VERSION: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings() 