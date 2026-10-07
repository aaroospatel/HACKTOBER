from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from app.config import settings

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}

engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all database tables on application startup."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency for yielding database sessions in FastAPI routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
