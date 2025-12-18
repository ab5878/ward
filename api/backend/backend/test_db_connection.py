#!/usr/bin/env python3
"""
Test database connection and diagnose issues
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
import socket

load_dotenv()

async def test_connection():
    print("🔍 Testing Supabase Database Connection\n")
    
    # Get connection string
    db_url = os.getenv("SUPABASE_DB_URL") or os.getenv("DATABASE_URL")
    
    if not db_url:
        print("❌ SUPABASE_DB_URL not found in environment")
        print("\n💡 Set it in backend/.env file:")
        print("   SUPABASE_DB_URL=postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:5432/postgres")
        return False
    
    print(f"✅ Connection string found (length: {len(db_url)})")
    
    # Parse connection string
    import re
    match = re.search(r'@([^:]+):?(\d+)?', db_url)
    if match:
        host = match.group(1)
        port = int(match.group(2)) if match.group(2) else 5432
        print(f"📍 Host: {host}")
        print(f"📍 Port: {port}")
        
        # Test DNS resolution
        print(f"\n🔍 Testing DNS resolution for {host}...")
        try:
            ip = socket.gethostbyname(host)
            print(f"✅ DNS resolved: {host} → {ip}")
        except socket.gaierror as e:
            print(f"❌ DNS resolution failed: {e}")
            print(f"\n💡 Possible issues:")
            print(f"   1. Check your internet connection")
            print(f"   2. Verify the hostname is correct: {host}")
            print(f"   3. Try using the Session Pooler connection string instead")
            return False
        
        # Test port connectivity
        print(f"\n🔍 Testing port connectivity to {host}:{port}...")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            sock.close()
            if result == 0:
                print(f"✅ Port {port} is reachable")
            else:
                print(f"❌ Port {port} is not reachable (error code: {result})")
                print(f"\n💡 Possible issues:")
                print(f"   1. Firewall blocking connection")
                print(f"   2. Supabase project might be paused")
                print(f"   3. Try using Session Pooler (port 6543) instead")
                return False
        except Exception as e:
            print(f"❌ Port test failed: {e}")
            return False
    else:
        print("❌ Could not parse connection string")
        return False
    
    # Test actual database connection
    print(f"\n🔍 Testing database connection...")
    try:
        from db_adapter import SupabaseAdapter
        
        adapter = SupabaseAdapter(db_url)
        await adapter.connect()
        print("✅ Database connection successful!")
        
        # Test a simple query
        result = await adapter.users_find_one({"email": "test@example.com"})
        print("✅ Test query successful")
        
        await adapter.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print(f"\n💡 Troubleshooting:")
        print(f"   1. Verify your password is correct")
        print(f"   2. Check if your Supabase project is active")
        print(f"   3. Try using Session Pooler connection string:")
        print(f"      Format: postgresql://postgres.[PROJECT-REF]:[PASSWORD]@[REGION].pooler.supabase.com:6543/postgres")
        print(f"   4. Get it from: Supabase Dashboard → Settings → Database → Connection Pooling")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_connection())
    sys.exit(0 if success else 1)

