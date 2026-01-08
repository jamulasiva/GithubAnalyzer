"""
Deploy database schema to Supabase.
This script will create all tables, indexes, RLS policies, and initial setup.
"""

import asyncio
import asyncpg
from pathlib import Path
from app.core.config import get_settings

async def deploy_schema():
    """Deploy the complete database schema to Supabase."""
    print("🚀 Deploying GitHub Audit Platform schema to Supabase...")
    
    settings = get_settings()
    
    # Extract connection details from DATABASE_URL
    # Format: postgresql+asyncpg://postgres:password@host:port/database
    db_url = settings.DATABASE_URL
    
    # Convert to asyncpg format (remove +asyncpg)
    asyncpg_url = db_url.replace("postgresql+asyncpg://", "postgresql://")
    
    # Read the schema file
    schema_file = Path(__file__).parent / "database_schema.sql"
    if not schema_file.exists():
        print("❌ database_schema.sql file not found!")
        return False
    
    schema_sql = schema_file.read_text()
    
    try:
        # Connect to Supabase
        print(f"📡 Connecting to Supabase: {settings.SUPABASE_URL}")
        conn = await asyncpg.connect(asyncpg_url)
        
        # Execute the schema
        print("📊 Creating tables and indexes...")
        await conn.execute(schema_sql)
        
        print("✅ Database schema deployed successfully!")
        
        # Verify tables were created
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        
        print(f"\n📋 Created {len(tables)} tables:")
        for table in tables:
            print(f"   ✅ {table['table_name']}")
        
        await conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Schema deployment failed: {e}")
        return False

async def main():
    """Main deployment function."""
    print("🔍 GitHub Audit Platform - Database Schema Deployment")
    print("=" * 60)
    
    success = await deploy_schema()
    
    if success:
        print("\n🎉 Database deployment complete!")
        print("\n📋 Next steps:")
        print("   1. Start the backend: python main.py")
        print("   2. Test webhooks: POST http://localhost:8000/api/v1/webhooks/github")
        print("   3. View API docs: http://localhost:8000/docs")
        print("   4. Monitor health: http://localhost:8000/health")
    else:
        print("\n⚠️  Database deployment failed. Check the error above.")

if __name__ == "__main__":
    asyncio.run(main())