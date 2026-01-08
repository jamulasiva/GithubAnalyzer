"""
Main API router for the GitHub Audit Platform.
Combines all API endpoints and provides versioned routing.
"""

from fastapi import APIRouter
from app.api import webhooks, audit

# Create main API router (prefix will be added in main.py)
api_router = APIRouter()

# Include sub-routers
api_router.include_router(webhooks.router)
api_router.include_router(audit.router)


@api_router.get("/")
async def api_info():
    """
    API information and available endpoints.
    """
    return {
        "name": "GitHub Audit Platform API",
        "version": "1.0.0",
        "description": "API for processing GitHub webhooks and providing audit analytics",
        "endpoints": {
            "webhooks": {
                "github": "/api/v1/webhooks/github",
                "events": "/api/v1/webhooks/github/events",
                "test": "/api/v1/webhooks/github/test"
            },
            "audit": {
                "organizations": "/api/v1/audit/organizations",
                "repositories": "/api/v1/audit/repositories", 
                "events": "/api/v1/audit/events",
                "analytics": "/api/v1/audit/analytics/summary"
            }
        },
        "documentation": {
            "interactive": "/docs",
            "openapi": "/openapi.json"
        }
    }


@api_router.get("/health")
async def health_check():
    """
    Detailed health check endpoint for monitoring.
    """
    from app.core.config import get_settings
    from app.core.database import check_database_connection
    import datetime
    
    settings = get_settings()
    
    # Check database connectivity
    db_status = "healthy"
    db_error = None
    try:
        await check_database_connection()
    except Exception as e:
        db_status = "unhealthy"
        db_error = str(e)
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "components": {
            "database": {
                "status": db_status,
                "error": db_error
            },
            "supabase": {
                "status": "configured" if settings.SUPABASE_URL and settings.SUPABASE_KEY else "not_configured"
            }
        },
        "version": "1.0.0"
    }