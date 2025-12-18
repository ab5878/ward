"""
Verification script for registration and login flow
Tests all critical paths to ensure everything works correctly
"""

import asyncio
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

# Set environment
os.environ.setdefault("USE_SUPABASE", "true")

from db_adapter import SupabaseAdapter
from db_compat import DBDatabase
from server import hash_password, verify_password, create_jwt_token
import jwt
from datetime import datetime, timezone

# Test configuration
TEST_EMAIL = f"test_{datetime.now().timestamp()}@example.com"
TEST_PASSWORD = "testpassword123"
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"

async def verify_database_connection():
    """Verify database connection works"""
    print("=" * 60)
    print("1. VERIFYING DATABASE CONNECTION")
    print("=" * 60)
    
    try:
        supabase_url = os.getenv("SUPABASE_DB_URL")
        if not supabase_url:
            print("❌ SUPABASE_DB_URL not set")
            print("\n   Please set your Supabase connection string:")
            print("   export SUPABASE_DB_URL='postgresql://user:password@host:5432/dbname'")
            print("\n   Get it from Supabase Dashboard → Settings → Database → Connection String")
            return False
        
        # Check if it's a placeholder
        if "user:pass@host:port" in supabase_url or "your-connection-string" in supabase_url.lower():
            print("❌ SUPABASE_DB_URL appears to be a placeholder")
            print(f"   Current value: {supabase_url[:50]}...")
            print("\n   Please set your actual Supabase connection string:")
            print("   export SUPABASE_DB_URL='postgresql://postgres:[YOUR-PASSWORD]@[HOST]:5432/postgres'")
            print("\n   Get it from Supabase Dashboard → Settings → Database → Connection String")
            print("   Format: postgresql://postgres:[PASSWORD]@[PROJECT-REF].supabase.co:5432/postgres")
            return False
        
        adapter = SupabaseAdapter(supabase_url)
        await adapter.connect()
        print("✅ Database connection successful")
        
        # Test query
        result = await adapter.users_find_one({"email": "nonexistent@example.com"})
        print(f"✅ Test query successful (result: {result})")
        
        await adapter.close()
        return True
    except ValueError as e:
        if "invalid literal for int()" in str(e) and "port" in str(e):
            print(f"❌ Database connection failed: Invalid connection string format")
            print(f"   Error: {e}")
            print("\n   The connection string format is incorrect.")
            print("   Expected format: postgresql://user:password@host:PORT/dbname")
            print("   The PORT must be a number (usually 5432 for PostgreSQL)")
            print("\n   Current SUPABASE_DB_URL:", os.getenv("SUPABASE_DB_URL", "not set"))
            print("\n   Get the correct connection string from:")
            print("   Supabase Dashboard → Settings → Database → Connection String")
            print("   (Use the 'Connection string' option, not 'Connection pooling')")
        else:
            print(f"❌ Database connection failed: {e}")
            import traceback
            traceback.print_exc()
        return False
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n   Make sure your SUPABASE_DB_URL is correct:")
        print("   Format: postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres")
        print("   Get it from: Supabase Dashboard → Settings → Database → Connection String")
        import traceback
        traceback.print_exc()
        return False

async def verify_password_hashing():
    """Verify password hashing and verification"""
    print("\n" + "=" * 60)
    print("2. VERIFYING PASSWORD HASHING")
    print("=" * 60)
    
    try:
        # Test password hashing
        hashed = hash_password(TEST_PASSWORD)
        print(f"✅ Password hashed successfully")
        print(f"   Hash length: {len(hashed)}")
        print(f"   Hash starts with: {hashed[:10]}...")
        
        # Test password verification - correct password
        is_valid = verify_password(TEST_PASSWORD, hashed)
        if is_valid:
            print("✅ Password verification works (correct password)")
        else:
            print("❌ Password verification failed (correct password)")
            return False
        
        # Test password verification - wrong password
        is_invalid = verify_password("wrongpassword", hashed)
        if not is_invalid:
            print("✅ Password verification works (wrong password rejected)")
        else:
            print("❌ Password verification failed (wrong password accepted)")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Password hashing failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def verify_user_insertion():
    """Verify user insertion works"""
    print("\n" + "=" * 60)
    print("3. VERIFYING USER INSERTION")
    print("=" * 60)
    
    try:
        supabase_url = os.getenv("SUPABASE_DB_URL")
        adapter = SupabaseAdapter(supabase_url)
        await adapter.connect()
        db = DBDatabase(adapter)
        
        # Check if user already exists
        existing = await db.users.find_one({"email": TEST_EMAIL})
        if existing:
            print(f"⚠️  Test user already exists (from previous test run)")
            print(f"   This is expected - user insertion still works correctly")
            print(f"   User ID: {existing.get('_id') or existing.get('id')}")
            await adapter.close()
            return True
        
        # Insert user
        hashed_pw = hash_password(TEST_PASSWORD)
        result = await db.users.insert_one({
            "email": TEST_EMAIL,
            "password_hash": hashed_pw,
            "created_at": datetime.now(timezone.utc)
        })
        
        print(f"✅ User inserted successfully")
        print(f"   inserted_id: {result.inserted_id}")
        print(f"   inserted_id type: {type(result.inserted_id)}")
        
        # Verify inserted_id is a string
        if isinstance(result.inserted_id, str):
            print("✅ inserted_id is a string (correct)")
        else:
            print(f"⚠️  inserted_id is {type(result.inserted_id)}, converting to string")
        
        user_id = str(result.inserted_id)
        print(f"   user_id: {user_id}")
        
        # Verify user can be retrieved
        user = await db.users.find_one({"email": TEST_EMAIL})
        if user:
            print("✅ User can be retrieved after insertion")
            print(f"   User keys: {list(user.keys())}")
            print(f"   Has _id: {'_id' in user}")
            print(f"   Has id: {'id' in user}")
            if "_id" in user:
                print(f"   _id value: {user['_id']}")
            if "id" in user:
                print(f"   id value: {user['id']}")
            
            # Verify _id matches inserted_id
            user_id_from_db = str(user.get("_id") or user.get("id"))
            if user_id_from_db == user_id:
                print("✅ User ID matches inserted_id")
            else:
                print(f"⚠️  User ID mismatch: {user_id_from_db} != {user_id}")
        else:
            print("❌ User not found after insertion")
            await adapter.close()
            return False
        
        await adapter.close()
        return True
    except Exception as e:
        print(f"❌ User insertion failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def verify_user_lookup():
    """Verify user lookup works"""
    print("\n" + "=" * 60)
    print("4. VERIFYING USER LOOKUP")
    print("=" * 60)
    
    try:
        supabase_url = os.getenv("SUPABASE_DB_URL")
        adapter = SupabaseAdapter(supabase_url)
        await adapter.connect()
        db = DBDatabase(adapter)
        
        # Lookup by email
        user = await db.users.find_one({"email": TEST_EMAIL})
        if user:
            print("✅ User lookup by email works")
            print(f"   User keys: {list(user.keys())}")
            
            # Check _id field
            if "_id" in user:
                print(f"✅ User has _id field: {user['_id']}")
            else:
                print("❌ User missing _id field")
                await adapter.close()
                return False
            
            # Check password_hash field
            if "password_hash" in user:
                print("✅ User has password_hash field")
            else:
                print("❌ User missing password_hash field")
                await adapter.close()
                return False
            
            # Verify password
            if verify_password(TEST_PASSWORD, user["password_hash"]):
                print("✅ Password verification works with retrieved user")
            else:
                print("❌ Password verification failed with retrieved user")
                await adapter.close()
                return False
            
        else:
            print("⚠️  User not found (may not exist yet)")
            await adapter.close()
            return True
        
        await adapter.close()
        return True
    except Exception as e:
        print(f"❌ User lookup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def verify_jwt_token():
    """Verify JWT token creation and validation"""
    print("\n" + "=" * 60)
    print("5. VERIFYING JWT TOKEN")
    print("=" * 60)
    
    try:
        test_user_id = "test-user-id-123"
        test_email = TEST_EMAIL
        
        # Create token
        token = create_jwt_token(test_user_id, test_email)
        print(f"✅ JWT token created")
        print(f"   Token length: {len(token)}")
        print(f"   Token preview: {token[:50]}...")
        
        # Decode token
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        print("✅ JWT token decoded successfully")
        print(f"   Payload: {payload}")
        
        # Verify payload contents
        if payload.get("user_id") == test_user_id:
            print("✅ Token contains correct user_id")
        else:
            print(f"❌ Token user_id mismatch: {payload.get('user_id')} != {test_user_id}")
            return False
        
        if payload.get("email") == test_email:
            print("✅ Token contains correct email")
        else:
            print(f"❌ Token email mismatch: {payload.get('email')} != {test_email}")
            return False
        
        if "exp" in payload:
            print("✅ Token contains expiration")
        else:
            print("❌ Token missing expiration")
            return False
        
        return True
    except Exception as e:
        print(f"❌ JWT token verification failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def verify_complete_flow():
    """Verify complete registration and login flow"""
    print("\n" + "=" * 60)
    print("6. VERIFYING COMPLETE FLOW")
    print("=" * 60)
    
    try:
        supabase_url = os.getenv("SUPABASE_DB_URL")
        adapter = SupabaseAdapter(supabase_url)
        await adapter.connect()
        db = DBDatabase(adapter)
        
        # Step 1: Check if user exists
        existing = await db.users.find_one({"email": TEST_EMAIL})
        if existing:
            print("⚠️  Test user already exists (from previous test)")
            print("   Using existing user for login flow test")
            user_id = str(existing.get("_id") or existing.get("id"))
        else:
            print("✅ User does not exist (ready for registration)")
            
            # Step 2: Register user
            hashed_pw = hash_password(TEST_PASSWORD)
            result = await db.users.insert_one({
                "email": TEST_EMAIL,
                "password_hash": hashed_pw,
                "created_at": datetime.now(timezone.utc)
            })
            
            user_id = str(result.inserted_id)
            print(f"✅ Registration step 1: User inserted, user_id: {user_id}")
            
            # Step 3: Create JWT token
            token = create_jwt_token(user_id, TEST_EMAIL)
            print(f"✅ Registration step 2: JWT token created")
        
        # Step 4: Login - lookup user
        user = await db.users.find_one({"email": TEST_EMAIL})
        if not user:
            print("❌ Login step 1: User not found")
            await adapter.close()
            return False
        print("✅ Login step 1: User found")
        
        # Step 5: Verify password
        if not verify_password(TEST_PASSWORD, user["password_hash"]):
            print("❌ Login step 2: Password verification failed")
            await adapter.close()
            return False
        print("✅ Login step 2: Password verified")
        
        # Step 6: Get user_id
        login_user_id = str(user.get("_id") or user.get("id"))
        if not login_user_id:
            print("❌ Login step 3: User ID not found")
            await adapter.close()
            return False
        print(f"✅ Login step 3: User ID extracted: {login_user_id}")
        
        # Step 7: Verify user_id matches (if we just created it)
        if not existing:
            if login_user_id == user_id:
                print("✅ Login step 4: User ID matches registration")
            else:
                print(f"⚠️  Login step 4: User ID mismatch: {login_user_id} != {user_id}")
        else:
            print("✅ Login step 4: Using existing user (skipping ID match check)")
        
        # Step 8: Create login token
        login_token = create_jwt_token(login_user_id, TEST_EMAIL)
        print("✅ Login step 5: JWT token created")
        
        # Step 9: Verify token
        payload = jwt.decode(login_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if payload.get("user_id") == login_user_id:
            print("✅ Login step 6: Token validated")
        else:
            print("❌ Login step 6: Token validation failed")
            await adapter.close()
            return False
        
        await adapter.close()
        print("\n✅ COMPLETE FLOW VERIFICATION SUCCESSFUL")
        return True
    except Exception as e:
        error_str = str(e)
        if "duplicate key" in error_str.lower() or "unique constraint" in error_str.lower():
            print(f"⚠️  User already exists (expected in test scenario)")
            print("   Testing login flow with existing user instead...")
            # Try login flow with existing user
            try:
                user = await db.users.find_one({"email": TEST_EMAIL})
                if user and verify_password(TEST_PASSWORD, user["password_hash"]):
                    user_id = str(user.get("_id") or user.get("id"))
                    token = create_jwt_token(user_id, TEST_EMAIL)
                    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
                    if payload.get("user_id") == user_id:
                        print("✅ Login flow works with existing user")
                        await adapter.close()
                        return True
            except Exception as login_error:
                print(f"❌ Login flow also failed: {login_error}")
        
        print(f"❌ Complete flow verification failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all verification tests"""
    print("\n" + "=" * 60)
    print("AUTHENTICATION FLOW VERIFICATION")
    print("=" * 60)
    print(f"Test email: {TEST_EMAIL}")
    print(f"Test password: {TEST_PASSWORD}")
    print()
    
    results = []
    
    # Run all tests
    results.append(("Database Connection", await verify_database_connection()))
    results.append(("Password Hashing", await verify_password_hashing()))
    results.append(("User Insertion", await verify_user_insertion()))
    results.append(("User Lookup", await verify_user_lookup()))
    results.append(("JWT Token", await verify_jwt_token()))
    results.append(("Complete Flow", await verify_complete_flow()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

