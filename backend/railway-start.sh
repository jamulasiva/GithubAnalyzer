#!/bin/bash

# Railway.com startup script
echo "🚀 Starting GitHub Analyzer Platform on Railway..."

# Set Python path
export PYTHONPATH=/app

# Create logs directory if it doesn't exist
mkdir -p logs

# Initialize database schema (Railway PostgreSQL)
echo "📊 Initializing database..."
python -c "
import asyncio
from app.core.database import init_database

async def main():
    try:
        await init_database()
        print('✅ Database initialized successfully')
    except Exception as e:
        print(f'⚠️ Database initialization error (may already exist): {e}')

asyncio.run(main())
"

# Start the application
echo "🎯 Starting FastAPI server..."
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1