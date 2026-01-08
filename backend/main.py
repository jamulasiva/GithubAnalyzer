"""
GitHub Audit Platform Backend

FastAPI application for receiving and processing GitHub webhooks with Supabase integration.
Includes real-time capabilities, audit trail, and analytics.
"""

from fastapi import FastAPI, Request, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer
import uvicorn
import os
from pathlib import Path

# Add the webhook_models to the Python path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from app.core.config import get_settings
from app.core.database import get_database
from app.core.logging_config import setup_logging
from app.api import api_router
from app.middleware.logging import LoggingMiddleware
from app.middleware.timing import TimingMiddleware

# Get settings
settings = get_settings()

# Initialize comprehensive logging FIRST (before any other imports that might log)
logger = setup_logging(settings.LOG_LEVEL)

# Initialize FastAPI app
app = FastAPI(
    title="GitHub Audit Platform",
    description="Real-time GitHub audit and compliance monitoring",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Log application startup
logger.info("🚀 Starting GitHub Audit Platform Backend")
logger.info(f"🔧 Environment: {os.getenv('ENVIRONMENT', 'development')}")
logger.info(f"🔧 Debug mode: {settings.DEBUG}")
logger.info(f"🔧 Host: {settings.HOST}:{settings.PORT}")

# Get configuration
settings = get_settings()

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

app.add_middleware(TimingMiddleware)
app.add_middleware(LoggingMiddleware)

# Add API routes
app.include_router(api_router, prefix="/api/v1")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    try:
        # Test database connection
        db = get_database()
        # Add basic connectivity test here
        
        return {
            "status": "healthy",
            "service": "github-audit-platform",
            "version": "1.0.0",
            "database": "connected"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "GitHub Audit Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )