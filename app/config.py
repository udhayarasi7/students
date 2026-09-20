import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Student Database Management System API"
    VERSION: str = "1.0.0"
    GROQ_API_KEY: str
    DATABASE_URL: str = "sqlite:///./students.db"
    CHROMA_PERSIST_DIR: str = "./chroma_data"

    class Config:
        env_file = ".env"

settings = Settings()