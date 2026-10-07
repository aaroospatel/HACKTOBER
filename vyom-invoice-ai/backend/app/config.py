from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional

class Settings(BaseSettings):
    gemini_api_key: str = ""
    openai_api_key: str = ""
    database_url: str = "sqlite:///./vyom_invoices.db"
    upload_dir: str = "./uploads"
    environment: str = "development"
    max_file_size_mb: int = 20
    confidence_threshold_high: float = 0.90
    confidence_threshold_review: float = 0.70

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
