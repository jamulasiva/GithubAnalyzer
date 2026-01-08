"""
Database configuration and connection management for Supabase.
Handles PostgreSQL connections, SQLAlchemy setup, and Supabase client integration.
"""

from functools import lru_cache
from typing import Generator, Optional
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.pool import StaticPool
import logging
from supabase import create_client, Client
from supabase.client import ClientOptions

from .config import get_settings

logger = logging.getLogger(__name__)

# SQLAlchemy setup
Base = declarative_base()
metadata = MetaData()

# Global variables for database connections
engine = None
SessionLocal = None
supabase_client = None


def create_database_engine():
    """Create SQLAlchemy engine for database connections."""
    global engine
    settings = get_settings()
    
    if not settings.DATABASE_URL:
        logger.warning("DATABASE_URL not configured. Database operations will fail.")
        return None
    
    # Create engine with appropriate settings
    engine_kwargs = {
        "pool_pre_ping": True,
        "pool_recycle": 3600,  # 1 hour
        "echo": settings.DEBUG,
    }
    
    # For SQLite (testing)
    if settings.DATABASE_URL.startswith("sqlite"):
        engine_kwargs.update({
            "poolclass": StaticPool,
            "connect_args": {"check_same_thread": False}
        })
    
    engine = create_engine(settings.DATABASE_URL, **engine_kwargs)
    return engine


def create_session_factory():
    """Create session factory for database operations."""
    global SessionLocal
    engine = create_database_engine()
    
    if engine is None:
        return None
    
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    return SessionLocal


def get_database() -> Generator[Session, None, None]:
    """
    Dependency for getting database session.
    Use this in FastAPI endpoints that need database access.
    """
    global SessionLocal
    
    if SessionLocal is None:
        SessionLocal = create_session_factory()
    
    if SessionLocal is None:
        raise RuntimeError("Database not configured")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@lru_cache()
def get_supabase_client() -> Optional[Client]:
    """
    Get Supabase client for real-time subscriptions and edge functions.
    Cached to avoid recreating the client.
    """
    global supabase_client
    settings = get_settings()
    
    if not settings.SUPABASE_URL or not settings.SUPABASE_ANON_KEY:
        logger.warning("Supabase credentials not configured. Real-time features will be disabled.")
        return None
    
    try:
        # Create client options
        options = ClientOptions(
            postgrest_client_timeout=10,
            storage_client_timeout=10,
        )
        
        supabase_client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_ANON_KEY,
            options=options
        )
        
        logger.info("Supabase client initialized successfully")
        return supabase_client
        
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")
        return None


def get_supabase_service_client() -> Optional[Client]:
    """
    Get Supabase client with service role key for admin operations.
    Used for bypassing RLS policies and administrative tasks.
    """
    settings = get_settings()
    
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_ROLE_KEY:
        logger.warning("Supabase service role credentials not configured.")
        return None
    
    try:
        service_client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_ROLE_KEY
        )
        
        logger.info("Supabase service client initialized successfully")
        return service_client
        
    except Exception as e:
        logger.error(f"Failed to initialize Supabase service client: {e}")
        return None


async def test_database_connection() -> bool:
    """Test database connection and return status."""
    try:
        db_generator = get_database()
        db = next(db_generator)
        
        # Simple query to test connection
        db.execute("SELECT 1")
        logger.info("Database connection test successful")
        return True
        
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False
    finally:
        try:
            db.close()
        except:
            pass


async def test_supabase_connection() -> bool:
    """Test Supabase connection and return status."""
    try:
        client = get_supabase_client()
        if not client:
            return False
        
        # Test connection with a simple query
        response = client.table("webhook_events").select("id").limit(1).execute()
        logger.info("Supabase connection test successful")
        return True
        
    except Exception as e:
        logger.error(f"Supabase connection test failed: {e}")
        return False


def create_tables():
    """Create database tables using SQLAlchemy metadata."""
    try:
        engine = create_database_engine()
        if engine is None:
            logger.error("Cannot create tables: database engine not initialized")
            return False
        
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        return False


# Initialize database on module import
def init_database():
    """Initialize database connections."""
    try:
        create_session_factory()
        get_supabase_client()
        logger.info("Database initialization completed")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")


# Database health check
async def check_database_connection():
    """Check if database connection is healthy."""
    return await DatabaseHealth.check_postgresql()


class DatabaseHealth:
    """Database health monitoring."""
    
    @staticmethod
    async def check_postgresql():
        """Check PostgreSQL connection health."""
        return await test_database_connection()
    
    @staticmethod
    async def check_supabase():
        """Check Supabase connection health."""
        return await test_supabase_connection()
    
    @staticmethod
    async def check_all():
        """Check all database connections."""
        postgresql_ok = await DatabaseHealth.check_postgresql()
        supabase_ok = await DatabaseHealth.check_supabase()
        
        return {
            "postgresql": postgresql_ok,
            "supabase": supabase_ok,
            "overall": postgresql_ok and supabase_ok
        }