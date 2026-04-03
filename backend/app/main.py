from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from .core.config import get_settings
from .core.database import Base, engine
from .api import projects, jobs

settings = get_settings()

# Create database tables
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
except Exception as e:
    print(f"⚠️  Database connection issue: {e}")
    print("Running in demo mode without database...")

# Create FastAPI app
app = FastAPI(
    title="AutoML Platform API",
    description="API for AutoML and Custom ML Training Platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories for uploads and models
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.MODELS_DIR, exist_ok=True)

# Mount static files for model downloads (will be implemented later)
# app.mount("/models", StaticFiles(directory=settings.MODELS_DIR), name="models")

# Include routers
app.include_router(projects.router, prefix="/api/v1/projects", tags=["Projects"])
app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["Jobs"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to AutoML Platform API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
