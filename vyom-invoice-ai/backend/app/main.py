from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routers import upload, invoice, export
from app.database.database import create_tables
from app.config import settings
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure upload directory exists and database tables are initialized
    os.makedirs(settings.upload_dir, exist_ok=True)
    create_tables()
    yield

app = FastAPI(
    title="VYOM+ — End-to-End AI-Powered GST Invoice Intelligence System",
    version="1.0.0",
    description="Intelligent GST document ingestion, multimodal AI extraction, deterministic statutory validation, and multi-format export API.",
    lifespan=lifespan
)

# CORS Middleware (allows Next.js frontend, Streamlit, and local requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(upload.router, prefix="/api")
app.include_router(invoice.router, prefix="/api")
app.include_router(export.router, prefix="/api")

@app.get("/")
def root():
    return {
        "title": "VYOM+ Invoice Intelligence API",
        "status": "running",
        "version": "1.0.0",
        "docs_url": "/docs"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "environment": settings.environment
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
