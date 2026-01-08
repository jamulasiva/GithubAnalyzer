"""
Test configuration and shared utilities for the test suite.
"""

import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Import the app and database dependencies
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from main import app
from app.core.database import get_database, Base

# Test database URL (SQLite for testing)
TEST_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create test session
TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=test_engine
)

def override_get_database():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override the dependency
app.dependency_overrides[get_database] = override_get_database

@pytest.fixture(scope="session")
def test_client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)

@pytest.fixture(scope="function")
def test_db():
    """Create a fresh database for each test."""
    # Create tables
    Base.metadata.create_all(bind=test_engine)
    yield TestingSessionLocal()
    # Drop tables
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def sample_headers():
    """Sample GitHub webhook headers."""
    return {
        "X-GitHub-Event": "push",
        "X-GitHub-Delivery": "test-delivery-id",
        "X-Hub-Signature-256": "sha256=test-signature",
        "User-Agent": "GitHub-Hookshot/test"
    }