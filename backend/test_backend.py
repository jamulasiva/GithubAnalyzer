"""
Simple backend validation test without webhook models dependency.
Tests core FastAPI functionality and basic imports.
"""

import sys
from pathlib import Path

def test_core_imports():
    """Test that core backend components can be imported."""
    try:
        # Test core FastAPI imports
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        print("✅ FastAPI imports successful")
        
        # Test database imports
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        print("✅ SQLAlchemy imports successful")
        
        # Test Supabase import
        from supabase import create_client
        print("✅ Supabase imports successful")
        
        # Test Pydantic
        from pydantic import BaseSettings
        print("✅ Pydantic v1 imports successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Core imports failed: {e}")
        return False


def test_app_imports():
    """Test that our app components can be imported."""
    try:
        from app.core.config import get_settings
        print("✅ App config imports successful")
        
        from app.core.database import get_database
        print("✅ App database imports successful")
        
        settings = get_settings()
        print(f"✅ Settings loaded: {settings.APP_NAME}")
        
        return True
        
    except Exception as e:
        print(f"❌ App imports failed: {e}")
        return False


def test_fastapi_app():
    """Test that FastAPI app can be created."""
    try:
        from fastapi import FastAPI
        
        app = FastAPI(
            title="Test App",
            version="1.0.0"
        )
        
        @app.get("/test")
        def test_endpoint():
            return {"status": "ok"}
        
        print("✅ FastAPI app creation successful")
        return True
        
    except Exception as e:
        print(f"❌ FastAPI app creation failed: {e}")
        return False


def main():
    """Run backend validation tests."""
    print("🔍 Backend Structure Validation")
    print("=" * 50)
    
    tests = [
        ("Core Imports", test_core_imports),
        ("App Imports", test_app_imports),
        ("FastAPI App", test_fastapi_app)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}")
        print("-" * 30)
        if test_func():
            passed += 1
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 Backend structure is valid! Ready for Supabase integration.")
        print("\n📋 Next Steps:")
        print("1. Set up Supabase project")
        print("2. Update .env with Supabase credentials")
        print("3. Run database schema in Supabase SQL editor")
        print("4. Start the backend with: python main.py")
    else:
        print("⚠️  Some tests failed. Check backend setup.")
        sys.exit(1)


if __name__ == "__main__":
    main()