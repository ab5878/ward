"""
Quick test script to diagnose registration issues
Run this to check if database and backend are working
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

load_dotenv()

async def test_database():
    """Test database connection and users table"""
    print("🔍 Testing database connection...")
    try:
        from db_adapter import SupabaseAdapter
        
        db_url = os.getenv("SUPABASE_DB_URL")
        if not db_url:
            print("❌ SUPABASE_DB_URL not found in environment")
            return False
        
        adapter = SupabaseAdapter(db_url)
        await adapter.connect()
        print("✅ Database connected")
        
        # Test if users table exists
        import asyncpg
        async with adapter.pool.acquire() as conn:
            # Check if users table exists
            result = await conn.fetchval("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'users'
                );
            """)
            
            if result:
                print("✅ Users table exists")
                
                # Try to query it
                count = await conn.fetchval("SELECT COUNT(*) FROM users")
                print(f"✅ Users table is accessible (current count: {count})")
                return True
            else:
                print("❌ Users table does NOT exist")
                print("   → Run the migration: supabase/migrations/001_initial_schema.sql")
                return False
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if 'adapter' in locals():
            await adapter.close()

async def test_registration_endpoint():
    """Test if registration endpoint would work"""
    print("\n🔍 Testing registration logic...")
    try:
        from db_adapter import SupabaseAdapter
        from db_compat import DBDatabase
        from server import hash_password
        from datetime import datetime, timezone
        
        db_url = os.getenv("SUPABASE_DB_URL")
        if not db_url:
            print("❌ SUPABASE_DB_URL not found")
            return False
        
        adapter = SupabaseAdapter(db_url)
        await adapter.connect()
        db = DBDatabase(adapter)
        
        # Test user lookup
        test_email = "test@example.com"
        existing = await db.users.find_one({"email": test_email})
        if existing:
            print(f"⚠️  Test user {test_email} already exists (this is OK)")
        else:
            print(f"✅ Test user lookup works (user doesn't exist)")
        
        # Test user insertion (then delete)
        test_user = {
            "email": f"test-{datetime.now().timestamp()}@example.com",
            "password_hash": hash_password("test123"),
            "created_at": datetime.now(timezone.utc)
        }
        
        result = await db.users.insert_one(test_user)
        user_id = str(result.inserted_id)
        print(f"✅ User insertion works (created test user: {user_id})")
        
        # Clean up test user
        # Note: We'd need a delete method, but for now just verify it was created
        print("✅ Registration logic test passed")
        
        await adapter.close()
        return True
        
    except Exception as e:
        print(f"❌ Registration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Ward Registration Diagnostic")
    print("=" * 50)
    print()
    
    # Test database
    db_ok = asyncio.run(test_database())
    
    if db_ok:
        # Test registration logic
        reg_ok = asyncio.run(test_registration_endpoint())
        
        if reg_ok:
            print("\n✅ All tests passed! Registration should work.")
        else:
            print("\n❌ Registration logic has issues. Check errors above.")
    else:
        print("\n❌ Database connection failed. Fix database issues first.")
        print("\nNext steps:")
        print("1. Run migration: supabase/migrations/001_initial_schema.sql")
        print("2. Check SUPABASE_DB_URL is correct")
        print("3. Check database password is correct")

